import json
from pathlib import Path

import pytest

from llm_repair import LLMRepairConfig, SingleLLMRepair
from llm_repair.patching import apply_edits, validate_proposal


class FakeLLM:
    def __init__(self, proposal):
        self.proposal = proposal
        self.messages = []

    def verify_model(self):
        return ["fake"]

    def chat_json(self, messages, schema, temperature=None, seed=None):
        self.messages.append(messages)
        return {
            "parsed": self.proposal,
            "raw_content": json.dumps(self.proposal),
            "metadata": {"seed": seed, "temperature": temperature},
        }


def patch_candidate(replacement="    return a + b"):
    return {
        "repair_intent": "Replace subtraction with a sum-producing implementation.",
        "assumption": "The function contract requires arithmetic addition.",
        "expected_effect": "Return the sum.",
        "preservation_constraints": ["Keep the function signature."],
        "edits": [{
            "start_line": 2,
            "end_line": 2,
            "replacement": replacement,
            "rationale": "Use addition.",
        }],
    }


def batch_proposal(replacements=None):
    replacements = replacements or ["    return a + b"]
    return {
        "diagnosis": "The arithmetic operator is inconsistent with the required sum.",
        "evidence_reasoning": {
            "testcase_refs": ["T1"],
            "mr_refs": [],
            "causal_chain": ["inputs reach line 2", "line 2 subtracts", "output is wrong"],
        },
        "uncertainty": "low",
        "repair_candidates": [patch_candidate(item) for item in replacements],
    }


def proposal(replacement="    return a + b"):
    return {
        "diagnosis": "The arithmetic operator is inconsistent with the required sum.",
        "evidence_reasoning": {
            "testcase_refs": ["T1"],
            "mr_refs": [],
            "causal_chain": ["inputs reach line 2", "line 2 subtracts", "output is wrong"],
        },
        "expected_effect": "Return the sum.",
        "preservation_constraints": ["Keep the function signature."],
        "uncertainty": "low",
        "edits": [{
            "start_line": 2,
            "end_line": 2,
            "replacement": replacement,
            "rationale": "Use addition.",
        }],
    }


def test_one_stage_repairs_and_compiles_python(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    tests = [{
        "test_id": "T1", "input": [2, 3], "actual_output": -1,
        "expected_output": 5, "test_status": "fail",
    }]
    fake = FakeLLM(batch_proposal())
    config = LLMRepairConfig(
        patch_budget=1, verify_ollama_model=False, max_generation_retries=0
    )
    result = SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=tests,
        mode="ORACLE",
        known_fault_line=2,
        output_dir=tmp_path / "out",
    )

    candidate = result["patch_candidates"][0]
    assert candidate["status"] == "compile_passed"
    assert "return a + b" in (tmp_path / "out/patches/P001/patched_faulty.py").read_text()
    assert result["workflow"] == "single_llm_direct_repair"
    prompt = fake.messages[0][1]["content"]
    assert '"evidence_mode": "ORACLE"' in prompt
    assert "Agent1" not in prompt
    assert "Agent2" not in prompt


def test_source_only_does_not_expose_test_or_mr_data(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    fake = FakeLLM(batch_proposal())
    config = LLMRepairConfig(
        patch_budget=1, verify_ollama_model=False, max_generation_retries=0
    )
    SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=[{"test_id": "SECRET_TEST", "expected_output": 5}],
        mg_relation=[{"mr_id": "SECRET_MR"}],
        mode="SOURCE_ONLY",
        output_dir=tmp_path / "out",
    )
    prompt = fake.messages[0][1]["content"]
    assert "SECRET_TEST" not in prompt
    assert "SECRET_MR" not in prompt


def test_mr_mode_requires_tests_and_relation(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("x = 1\n", encoding="utf-8")
    config = LLMRepairConfig(patch_budget=1, verify_ollama_model=False)
    with pytest.raises(ValueError, match="MR mode requires"):
        SingleLLMRepair(config, FakeLLM(batch_proposal())).run(
            source, "Set x.", mode="MR", output_dir=tmp_path / "out"
        )


def test_mr_mode_removes_accidental_oracle_information(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    fake = FakeLLM(batch_proposal())
    config = LLMRepairConfig(
        patch_budget=1, verify_ollama_model=False, max_generation_retries=0
    )
    SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=[{
            "test_id": "T1", "input": [2, 3], "actual_output": -1,
            "expected_output": "SECRET_ORACLE", "test_status": "fail",
        }],
        mg_relation=[{
            "mr_id": "MR1", "source_test_id": "T1",
            "followup_test_id": "T1", "actual_relation_status": "VMG",
        }],
        mode="MR",
        output_dir=tmp_path / "out",
    )
    prompt = fake.messages[0][1]["content"]
    assert "SECRET_ORACLE" not in prompt
    assert '"test_status": "unknown"' in prompt


def test_overlapping_edits_are_rejected():
    item = proposal()
    item["edits"].append({
        "start_line": 2, "end_line": 2, "replacement": "    return 0",
        "rationale": "conflict",
    })
    config = LLMRepairConfig(verify_ollama_model=False)
    errors = validate_proposal(item, "def f():\n    return 1\n", [], config)
    assert "edit ranges overlap" in errors


def test_multiple_edits_use_original_line_numbers():
    source = "a\nb\nc\nd\n"
    patched = apply_edits(source, [
        {"start_line": 2, "end_line": 2, "replacement": "B1\nB2"},
        {"start_line": 4, "end_line": 4, "replacement": "D"},
    ])
    assert patched == "a\nB1\nB2\nc\nD\n"


def test_five_patches_are_returned_by_one_model_call(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    replacements = [
        "    return a + b",
        "    return b + a",
        "    return sum((a, b))",
        "    return a - (-b)",
        "    result = a + b\n    return result",
    ]
    fake = FakeLLM(batch_proposal(replacements))
    config = LLMRepairConfig(
        patch_budget=5, verify_ollama_model=False, max_generation_retries=0
    )
    result = SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=[{
            "test_id": "T1", "input": [2, 3], "actual_output": -1,
            "expected_output": 5, "test_status": "fail",
        }],
        mode="ORACLE",
        known_fault_line=2,
        output_dir=tmp_path / "out",
    )

    assert len(fake.messages) == 1
    assert len(result["patch_candidates"]) == 5
    assert result["llm_call_attempts"] == 1
    assert result["normal_llm_calls_per_scenario"] == 1
    assert all(item["status"] == "compile_passed" for item in result["patch_candidates"])


def test_five_identical_patches_are_allowed_and_preserved(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    fake = FakeLLM(batch_proposal(["    return a + b"] * 5))
    config = LLMRepairConfig(
        patch_budget=5, verify_ollama_model=False, max_generation_retries=0
    )
    result = SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=[{
            "test_id": "T1", "input": [2, 3], "actual_output": -1,
            "expected_output": 5, "test_status": "fail",
        }],
        mode="ORACLE",
        known_fault_line=2,
        output_dir=tmp_path / "out",
    )

    candidates = result["patch_candidates"]
    assert len(fake.messages) == 1
    assert len(candidates) == 5
    assert all(item["status"] == "compile_passed" for item in candidates)
    assert candidates[0]["duplicate_of"] is None
    assert [item["duplicate_of"] for item in candidates[1:]] == ["P001"] * 4
    assert [item["validation_reused_from"] for item in candidates[1:]] == ["P001"] * 4
    assert result["summary"]["duplicates"] == 4


def test_invalid_non_anchor_candidate_is_replaced_without_recalling_llm(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text(
        "def add(a, b):\n    value = a - b\n    return value\n",
        encoding="utf-8",
    )
    payload = batch_proposal(["    value = a + b"] * 5)
    payload["repair_candidates"][2]["edits"] = [{
        "start_line": 3,
        "end_line": 3,
        "replacement": "    return a + b",
        "rationale": "Edits the wrong line for this known-line experiment.",
    }]
    fake = FakeLLM(payload)
    config = LLMRepairConfig(
        patch_budget=5, verify_ollama_model=False, max_generation_retries=0
    )
    result = SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=[{
            "test_id": "T1", "input": [2, 3], "actual_output": -1,
            "expected_output": 5, "test_status": "fail",
        }],
        mode="ORACLE",
        known_fault_line=2,
        output_dir=tmp_path / "out",
    )

    candidates = result["patch_candidates"]
    assert len(fake.messages) == 1
    assert len(candidates) == 5
    assert candidates[2]["fallback_copy_of"] == "P001"
    assert any(
        "no edit covers a known fault line" in error
        for error in candidates[2]["original_candidate_errors"]
    )
    assert all(item["status"] == "compile_passed" for item in candidates)


def test_missing_candidate_slots_are_filled_from_a_valid_candidate(tmp_path):
    source = tmp_path / "faulty.py"
    source.write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    fake = FakeLLM(batch_proposal([
        "    return a + b",
        "    return b + a",
    ]))
    config = LLMRepairConfig(
        patch_budget=5, verify_ollama_model=False, max_generation_retries=0
    )
    result = SingleLLMRepair(config, fake).run(
        program_path=source,
        program_function="Return a plus b.",
        test_executions=[{
            "test_id": "T1", "input": [2, 3], "actual_output": -1,
            "expected_output": 5, "test_status": "fail",
        }],
        mode="ORACLE",
        known_fault_line=2,
        output_dir=tmp_path / "out",
    )

    candidates = result["patch_candidates"]
    assert len(fake.messages) == 1
    assert len(candidates) == 5
    assert [item["fallback_copy_of"] for item in candidates[2:]] == ["P001"] * 3
    assert all(item["status"] == "compile_passed" for item in candidates)
