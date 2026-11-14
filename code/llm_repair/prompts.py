import json


VALID_MODES = {"SOURCE_ONLY", "ORACLE", "MR", "ORACLE_MR", "AUTO"}


def proposal_schema(max_edits, patch_count):
    edit_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["start_line", "end_line", "replacement", "rationale"],
        "properties": {
            "start_line": {"type": "integer", "minimum": 1},
            "end_line": {"type": "integer", "minimum": 1},
            "replacement": {"type": "string"},
            "rationale": {"type": "string"},
        },
    }
    candidate_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "repair_intent", "assumption", "expected_effect",
            "preservation_constraints", "edits",
        ],
        "properties": {
            "repair_intent": {"type": "string"},
            "assumption": {"type": "string"},
            "expected_effect": {"type": "string"},
            "preservation_constraints": {
                "type": "array", "items": {"type": "string"}
            },
            "edits": {
                "type": "array",
                "minItems": 1,
                "maxItems": int(max_edits),
                "items": edit_schema,
            },
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "diagnosis", "evidence_reasoning", "uncertainty",
            "repair_candidates",
        ],
        "properties": {
            "diagnosis": {"type": "string"},
            "evidence_reasoning": {
                "type": "object",
                "additionalProperties": False,
                "required": ["testcase_refs", "mr_refs", "causal_chain"],
                "properties": {
                    "testcase_refs": {"type": "array", "items": {"type": "string"}},
                    "mr_refs": {"type": "array", "items": {"type": "string"}},
                    "causal_chain": {"type": "array", "items": {"type": "string"}},
                },
            },
            "uncertainty": {"type": "string"},
            "repair_candidates": {
                "type": "array",
                "minItems": int(patch_count),
                "maxItems": int(patch_count),
                "items": candidate_schema,
            },
        },
    }


def _numbered_source(source_text):
    return "\n".join(
        "{:>5} | {}".format(index, line)
        for index, line in enumerate(source_text.splitlines(), 1)
    )


def build_messages(
    source_text,
    source_name,
    program_function,
    mode,
    tests,
    relations,
    known_fault_lines,
    max_edits,
    patch_count,
    previous_errors=None,
):
    system = """You are a program repair model, not one stage in a multi-agent pipeline.
In this single response, analyze the supplied source and permitted evidence exactly
once, then derive all requested repair candidates from that shared analysis. Follow the
JSON schema exactly. Do not ask for another analysis stage.

Evidence rules:
1. Do not invent expected outputs, executions, MR violations, or hidden requirements.
2. A failing oracle testcase may constrain the required output. A passing testcase is
   a preservation constraint. A missing expected output is not an oracle.
3. For MR evidence, explicitly connect: input transformation -> required output
   relation -> observed violation -> relevant source mechanism. An MR violation narrows
   behavior but does not by itself prove a particular statement is faulty.
4. If evidence is weak or permits multiple explanations, say so in uncertainty. Explore
   different plausible repair directions only when the evidence supports them. Never
   reduce likely correctness merely to make candidates look different.
5. replacement must contain literal source text only, without Markdown fences or line
   numbers. Every range refers to the ORIGINAL numbered source. Keep unrelated behavior.
6. When known_fault_lines is non-empty, every candidate must include at least one edit
   whose original-source range covers a known fault line. These are mandatory repair
   anchors. A candidate may additionally edit nearby causally necessary statements, but
   it must not replace the required anchor with an unrelated location.
7. Return exactly the requested number of repair_candidates in this one response. Insofar
   as correctness is preserved, make candidates different to cover plausible alternatives.
   If the defect and correct repair are clear, candidates may have identical repair intents
   and identical edits. Never invent unsupported repairs to force diversity. Every
   candidate starts from the ORIGINAL source.
"""
    payload = {
        "task": "Analyze once and directly produce all patch candidates in one LLM response.",
        "source_file": source_name,
        "intended_function": program_function,
        "evidence_mode": mode,
        "known_fault_lines": known_fault_lines,
        "test_executions": tests,
        "metamorphic_relations": relations,
        "maximum_edit_blocks_per_candidate": max_edits,
        "required_patch_candidates": int(patch_count),
        "source_with_line_numbers": _numbered_source(source_text),
    }
    if previous_errors:
        payload["previous_response_errors"] = previous_errors
        payload["retry_instruction"] = (
            "Correct the whole batch's structural/range errors while keeping one shared analysis."
        )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, indent=2)},
    ]
