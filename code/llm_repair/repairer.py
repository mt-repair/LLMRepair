import hashlib
import shutil
from pathlib import Path

from .config import LLMRepairConfig
from .executor import prepare_workspace, validate_candidate
from .io_utils import load_json, save_json, tail_text
from .llm import OllamaClient, OllamaJSONError
from .patching import (
    apply_edits,
    unified_diff,
    validate_batch_proposal,
    validate_repair_candidate,
)
from .prompts import VALID_MODES, build_messages, proposal_schema


def _normalize_lines(value):
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple, set)) else [value]
    result = []
    for item in values:
        if isinstance(item, bool):
            raise ValueError("known_fault_line must contain positive integers")
        number = int(item)
        if number <= 0:
            raise ValueError("known_fault_line must contain positive integers")
        if number not in result:
            result.append(number)
    return sorted(result)


def _has_oracle(test):
    if not isinstance(test, dict):
        return False
    expected = test.get("expected_output")
    return expected is not None and str(expected).strip().lower() not in {
        "", "missing", "unknown", "none", "null", "n/a"
    }


def _remove_oracle_information(tests):
    """Prevent accidental oracle leakage into an MR-only experiment."""
    oracle_keys = {
        "expected", "expected_output", "oracle", "oracle_output",
        "ground_truth", "correct_output",
    }
    sanitized = []
    for test in tests:
        if not isinstance(test, dict):
            sanitized.append(test)
            continue
        item = {
            key: value
            for key, value in test.items()
            if str(key).lower() not in oracle_keys
        }
        if "test_status" in item:
            item["test_status"] = "unknown"
        sanitized.append(item)
    return sanitized


def _prepare_evidence(mode, tests, relations):
    mode = str(mode).upper()
    if mode not in VALID_MODES:
        raise ValueError("mode must be one of {}".format(sorted(VALID_MODES)))
    tests = tests or []
    relations = relations or []
    if not isinstance(tests, list):
        raise ValueError("test_executions JSON must be an array")
    if not isinstance(relations, list):
        raise ValueError("mg_relation JSON must be an array")

    if mode == "AUTO":
        has_oracle = any(_has_oracle(test) for test in tests)
        has_mr = bool(relations)
        mode = (
            "ORACLE_MR" if has_oracle and has_mr
            else "ORACLE" if has_oracle
            else "MR" if has_mr
            else "SOURCE_ONLY"
        )
    if mode == "SOURCE_ONLY":
        return mode, [], []
    if mode == "ORACLE":
        oracle_tests = [test for test in tests if _has_oracle(test)]
        if not oracle_tests:
            raise ValueError("ORACLE mode requires at least one expected_output")
        return mode, oracle_tests, []
    if mode == "MR":
        if not tests or not relations:
            raise ValueError("MR mode requires test_executions and mg_relation")
        return mode, _remove_oracle_information(tests), relations
    if not any(_has_oracle(test) for test in tests) or not relations:
        raise ValueError("ORACLE_MR mode requires oracle outputs and MR data")
    return mode, tests, relations


class SingleLLMRepair:
    """One-stage repair: evidence and source go directly to one repair model."""

    def __init__(self, config=None, llm_client=None):
        self.config = config or LLMRepairConfig()
        self.config.validate()
        self.llm = llm_client or OllamaClient(self.config)

    def run(
        self,
        program_path,
        program_function,
        test_executions=None,
        mg_relation=None,
        mode="AUTO",
        known_fault_line=None,
        output_dir="llm_output",
        project_root=None,
        compile_command=None,
        visible_checks=None,
        patch_budget=None,
    ):
        program_path = Path(program_path).absolute()
        if not program_path.is_file():
            raise FileNotFoundError("program_path does not exist: {}".format(program_path))
        project_root = Path(project_root).absolute() if project_root else program_path.parent
        try:
            program_path.relative_to(project_root)
        except ValueError as exc:
            raise ValueError("program_path must be inside project_root") from exc
        output_dir = Path(output_dir).absolute()
        output_dir.mkdir(parents=True, exist_ok=True)

        source_text = program_path.read_text(encoding="utf-8-sig")
        known_lines = _normalize_lines(known_fault_line)
        line_count = len(source_text.splitlines())
        if any(line > line_count for line in known_lines):
            raise ValueError("known_fault_line is outside the source file")
        requested_mode = str(mode).upper()
        if requested_mode not in VALID_MODES:
            raise ValueError("mode must be one of {}".format(sorted(VALID_MODES)))
        # Do not even read evidence that is forbidden by the selected ablation.
        tests = (
            [] if requested_mode == "SOURCE_ONLY"
            else (load_json(test_executions, "test_executions") or [])
        )
        relations = (
            load_json(mg_relation, "mg_relation") or []
            if requested_mode in {"MR", "ORACLE_MR", "AUTO"}
            else []
        )
        effective_mode, tests, relations = _prepare_evidence(
            requested_mode, tests, relations
        )
        budget = self.config.patch_budget if patch_budget is None else int(patch_budget)
        if budget <= 0:
            raise ValueError("patch_budget must be > 0")

        run_input = {
            "program_path": str(program_path),
            "project_root": str(project_root),
            "program_function": str(program_function),
            "requested_mode": requested_mode,
            "effective_mode": effective_mode,
            "known_fault_lines": known_lines,
            "test_executions": tests,
            "mg_relation": relations,
            "patch_budget": budget,
            "generation_limits": {
                "num_ctx": self.config.num_ctx,
                "num_predict": self.config.num_predict,
                "max_edits_per_candidate": self.config.max_edits,
                "max_total_touched_lines_per_candidate": (
                    self.config.max_total_touched_lines
                ),
                "require_known_line_coverage": (
                    self.config.require_known_line_coverage
                ),
            },
            "policy": (
                "One LLM response performs one shared evidence analysis and returns "
                "all patch candidates; no Agent1/Agent2 artifacts are used."
            ),
        }
        save_json(output_dir / "00_repair_input.json", run_input)
        if self.config.verify_ollama_model:
            self.llm.verify_model()

        # One normal model call returns the shared analysis and the whole patch batch.
        # Retries occur only when that entire response is malformed or invalid.
        schema = proposal_schema(self.config.max_edits, budget)
        batch_proposal = None
        response = None
        errors = []
        attempts = []
        previous_errors = []
        for attempt in range(1, self.config.max_generation_retries + 2):
            messages = build_messages(
                source_text=source_text,
                source_name=program_path.name,
                program_function=str(program_function),
                mode=effective_mode,
                tests=tests,
                relations=relations,
                known_fault_lines=known_lines,
                max_edits=self.config.max_edits,
                patch_count=budget,
                previous_errors=previous_errors,
            )
            try:
                response = self.llm.chat_json(
                    messages,
                    schema,
                    temperature=self.config.temperature,
                    seed=self.config.seed + attempt - 1,
                )
                batch_proposal = response["parsed"]
                errors = validate_batch_proposal(
                    batch_proposal,
                    source_text,
                    known_lines,
                    self.config,
                    budget,
                )
                attempts.append({
                    "attempt": attempt,
                    "errors": errors,
                    "response_metadata": response.get("metadata", {}),
                })
                if not errors:
                    break
                previous_errors = errors
            except OllamaJSONError as exc:
                errors = [str(exc)]
                previous_errors = errors
                attempts.append({
                    "attempt": attempt,
                    "errors": errors,
                    "raw_tail": tail_text(exc.raw_content, 1000),
                    "response_metadata": exc.metadata,
                })
            except Exception as exc:
                errors = ["{}: {}".format(type(exc).__name__, exc)]
                previous_errors = errors
                attempts.append({"attempt": attempt, "errors": errors})

        save_json(output_dir / "01_generation_attempts.json", attempts)
        materialized_candidates = []
        normalization = {
            "requested_candidates": budget,
            "model_returned_candidates": 0,
            "valid_model_candidates": 0,
            "invalid_model_candidates": 0,
            "ignored_extra_candidates": 0,
            "candidate_assessments": [],
            "output_slots": [],
        }
        if not errors and batch_proposal is not None:
            raw_candidates = batch_proposal.get("repair_candidates", [])
            normalization["model_returned_candidates"] = len(raw_candidates)
            valid_candidates = []
            errors_by_index = {}
            for index, patch_proposal in enumerate(raw_candidates):
                source_patch_id = "P{:03d}".format(index + 1)
                candidate_errors = validate_repair_candidate(
                    patch_proposal,
                    source_text,
                    known_lines,
                    self.config,
                    "repair_candidates[{}].".format(index),
                )
                errors_by_index[index] = candidate_errors
                is_valid = not candidate_errors
                normalization["candidate_assessments"].append({
                    "model_candidate": source_patch_id,
                    "accepted": is_valid,
                    "errors": candidate_errors,
                    "within_requested_budget": index < budget,
                })
                if is_valid:
                    valid_candidates.append((index, patch_proposal))

            normalization["valid_model_candidates"] = len(valid_candidates)
            normalization["invalid_model_candidates"] = sum(
                bool(item["errors"])
                for item in normalization["candidate_assessments"]
            )
            normalization["ignored_extra_candidates"] = max(
                0, len(raw_candidates) - budget
            )

            if not valid_candidates:
                errors = [
                    "The LLM response contained no valid repair candidate; "
                    "there is no safe candidate to copy into invalid slots."
                ]
                if attempts:
                    attempts[-1]["post_generation_errors"] = errors
                    save_json(output_dir / "01_generation_attempts.json", attempts)
            else:
                fallback_index, fallback_proposal = valid_candidates[0]
                fallback_id = "P{:03d}".format(fallback_index + 1)
                for output_index in range(budget):
                    output_id = "P{:03d}".format(output_index + 1)
                    own_proposal = (
                        raw_candidates[output_index]
                        if output_index < len(raw_candidates)
                        else None
                    )
                    own_errors = errors_by_index.get(
                        output_index,
                        ["model did not return this candidate slot"],
                    )
                    if own_proposal is not None and not own_errors:
                        selected_proposal = own_proposal
                        selected_source_id = output_id
                        fallback_copy_of = None
                    else:
                        selected_proposal = fallback_proposal
                        selected_source_id = fallback_id
                        fallback_copy_of = fallback_id
                    materialized_candidates.append({
                        "patch_proposal": selected_proposal,
                        "model_candidate_source": selected_source_id,
                        "fallback_copy_of": fallback_copy_of,
                        "original_candidate_errors": own_errors,
                    })
                    normalization["output_slots"].append({
                        "patch_id": output_id,
                        "model_candidate_source": selected_source_id,
                        "fallback_copy_of": fallback_copy_of,
                        "original_candidate_errors": own_errors,
                    })

        if batch_proposal is not None:
            save_json(output_dir / "02_llm_analysis_and_repairs.json", batch_proposal)
        save_json(output_dir / "03_candidate_normalization.json", normalization)
        candidates = []
        seen_results = {}
        if errors or batch_proposal is None:
            for slot in range(1, budget + 1):
                patch_id = "P{:03d}".format(slot)
                candidate_dir = output_dir / "patches" / patch_id
                candidate_dir.mkdir(parents=True, exist_ok=True)
                candidate = {
                    "patch_id": patch_id,
                    "status": "generation_failed",
                    "proposal": None,
                    "proposal_errors": errors,
                    "patch_diff": "",
                    "patch_hash": None,
                    "model_candidate_source": None,
                    "fallback_copy_of": None,
                    "original_candidate_errors": [],
                    "duplicate_of": None,
                    "validation_reused_from": None,
                    "validation": None,
                }
                save_json(candidate_dir / "candidate.json", candidate)
                candidates.append(candidate)
        else:
            shared_analysis = {
                "diagnosis": batch_proposal["diagnosis"],
                "evidence_reasoning": batch_proposal["evidence_reasoning"],
                "uncertainty": batch_proposal["uncertainty"],
            }
            for slot, materialized in enumerate(materialized_candidates, 1):
                patch_proposal = materialized["patch_proposal"]
                patch_id = "P{:03d}".format(slot)
                candidate_dir = output_dir / "patches" / patch_id
                candidate_dir.mkdir(parents=True, exist_ok=True)
                proposal = dict(shared_analysis)
                proposal.update(patch_proposal)
                candidate = {
                    "patch_id": patch_id,
                    "status": "generated",
                    "proposal": proposal,
                    "proposal_errors": [],
                    "patch_diff": "",
                    "patch_hash": None,
                    "model_candidate_source": materialized["model_candidate_source"],
                    "fallback_copy_of": materialized["fallback_copy_of"],
                    "original_candidate_errors": materialized[
                        "original_candidate_errors"
                    ],
                    "duplicate_of": None,
                    "validation_reused_from": None,
                    "validation": None,
                }
                save_json(candidate_dir / "proposal.json", proposal)
                patched_text = apply_edits(source_text, patch_proposal["edits"])
                diff_text = unified_diff(source_text, patched_text, program_path.name)
                patch_hash = hashlib.sha256(diff_text.encode("utf-8")).hexdigest()
                candidate["patch_diff"] = diff_text
                candidate["patch_hash"] = patch_hash
                (candidate_dir / "patch.diff").write_text(diff_text, encoding="utf-8")
                (candidate_dir / ("patched_" + program_path.name)).write_text(
                    patched_text, encoding="utf-8"
                )
                if patch_hash in seen_results:
                    previous = seen_results[patch_hash]
                    candidate["duplicate_of"] = previous["patch_id"]
                    candidate["validation_reused_from"] = previous["patch_id"]
                    candidate["validation"] = previous["validation"]
                    candidate["status"] = previous["status"]
                    save_json(candidate_dir / "candidate.json", candidate)
                    candidates.append(candidate)
                    continue

                workspace = None
                try:
                    workspace, copied_source = prepare_workspace(
                        program_path, project_root, candidate_dir, output_dir
                    )
                    copied_source.write_text(patched_text, encoding="utf-8")
                    validation = validate_candidate(
                        copied_source,
                        workspace,
                        compile_command,
                        visible_checks,
                        self.config.compile_timeout,
                        self.config.check_timeout,
                    )
                    candidate["validation"] = validation
                    compile_ok = validation["compile"].get("success")
                    check_results = validation["visible_checks"]
                    checks_ok = all(
                        item.get("success") is True for item in check_results
                    )
                    if compile_ok is False:
                        candidate["status"] = "compile_failed"
                    elif check_results and not checks_ok:
                        candidate["status"] = "visible_check_failed"
                    elif check_results:
                        candidate["status"] = "visible_checks_passed"
                    elif compile_ok is True:
                        candidate["status"] = "compile_passed"
                    else:
                        candidate["status"] = "generated_uncompiled"
                except Exception as exc:
                    candidate["status"] = "validation_error"
                    candidate["validation"] = {
                        "error": "{}: {}".format(type(exc).__name__, exc)
                    }
                finally:
                    if (
                        workspace
                        and workspace.exists()
                        and not self.config.keep_workspaces
                    ):
                        shutil.rmtree(workspace)
                seen_results[patch_hash] = {
                    "patch_id": patch_id,
                    "status": candidate["status"],
                    "validation": candidate["validation"],
                }
                save_json(candidate_dir / "candidate.json", candidate)
                candidates.append(candidate)

        result = {
            "workflow": "single_llm_direct_repair",
            "effective_mode": effective_mode,
            "program_path": str(program_path),
            "output_dir": str(output_dir),
            "llm_call_attempts": len(attempts),
            "normal_llm_calls_per_scenario": 1,
            "patch_candidates": candidates,
            "summary": {
                "requested": budget,
                "generated": sum(c.get("proposal") is not None for c in candidates),
                "compile_passed": sum(c["status"] in {"compile_passed", "visible_checks_passed"} for c in candidates),
                "visible_checks_passed": sum(c["status"] == "visible_checks_passed" for c in candidates),
                "fallback_filled": sum(c.get("fallback_copy_of") is not None for c in candidates),
                "duplicates": sum(c.get("duplicate_of") is not None for c in candidates),
                "failed": sum(c["status"] in {"generation_failed", "compile_failed", "visible_check_failed", "validation_error"} for c in candidates),
            },
            "interpretation": "Compilation only proves syntactic/build validity. Semantic repair success requires independent hidden tests or an external evaluator.",
        }
        save_json(output_dir / "04_patch_candidates.json", candidates)
        save_json(output_dir / "llm_repair_result.json", result)
        return result


def run_llm_repair(
    program_path,
    program_function,
    test_executions=None,
    mg_relation=None,
    mode="AUTO",
    known_fault_line=None,
    output_dir="llm_output",
    project_root=None,
    compile_command=None,
    visible_checks=None,
    patch_budget=5,
    model="deepcoder:14b",
    ollama_host="http://localhost:11434",
    temperature=0.05,
    seed=0,
    num_ctx=32768,
    num_predict=8192,
    timeout=900,
    max_generation_retries=0,
    max_edits=3,
    max_total_touched_lines=20,
    require_known_line_coverage=True,
    compile_timeout=60,
    check_timeout=10,
    keep_workspaces=False,
    verify_ollama_model=True,
):
    config = LLMRepairConfig(
        model=model,
        ollama_host=ollama_host,
        temperature=temperature,
        seed=seed,
        num_ctx=num_ctx,
        num_predict=num_predict,
        timeout=timeout,
        patch_budget=patch_budget,
        max_generation_retries=max_generation_retries,
        max_edits=max_edits,
        max_total_touched_lines=max_total_touched_lines,
        require_known_line_coverage=require_known_line_coverage,
        compile_timeout=compile_timeout,
        check_timeout=check_timeout,
        keep_workspaces=keep_workspaces,
        verify_ollama_model=verify_ollama_model,
    )
    return SingleLLMRepair(config=config).run(
        program_path=program_path,
        program_function=program_function,
        test_executions=test_executions,
        mg_relation=mg_relation,
        mode=mode,
        known_fault_line=known_fault_line,
        output_dir=output_dir,
        project_root=project_root,
        compile_command=compile_command,
        visible_checks=visible_checks,
        patch_budget=patch_budget,
    )
