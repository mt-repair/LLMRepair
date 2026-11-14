import difflib


def apply_edits(source_text, edits):
    """Apply non-overlapping original-line edits from bottom to top."""
    had_final_newline = source_text.endswith("\n")
    lines = source_text.splitlines()
    for edit in sorted(edits, key=lambda item: int(item["start_line"]), reverse=True):
        start = int(edit["start_line"])
        end = int(edit["end_line"])
        replacement = str(edit.get("replacement", "")).splitlines()
        lines[start - 1:end] = replacement
    result = "\n".join(lines)
    if had_final_newline:
        result += "\n"
    return result


def unified_diff(original, patched, name):
    return "".join(difflib.unified_diff(
        original.splitlines(keepends=True),
        patched.splitlines(keepends=True),
        fromfile="a/{}".format(name),
        tofile="b/{}".format(name),
    ))


def _validate_edits(edits, source_text, known_fault_lines, config, prefix=""):
    errors = []
    if not isinstance(edits, list) or not edits:
        return ["{}edits must contain at least one edit".format(prefix)]
    if len(edits) > config.max_edits:
        errors.append("{}too many edits: {} > {}".format(
            prefix, len(edits), config.max_edits
        ))

    line_count = len(source_text.splitlines())
    ranges = []
    touched = 0
    for index, edit in enumerate(edits):
        if not isinstance(edit, dict):
            errors.append("{}edits[{}] must be an object".format(prefix, index))
            continue
        try:
            start = int(edit["start_line"])
            end = int(edit["end_line"])
        except (KeyError, TypeError, ValueError):
            errors.append("{}edits[{}] has an invalid range".format(prefix, index))
            continue
        if start < 1 or end < start or end > line_count:
            errors.append("{}edits[{}] range is outside the source".format(prefix, index))
            continue
        if "replacement" not in edit:
            errors.append("{}edits[{}] is missing replacement".format(prefix, index))
        ranges.append((start, end))
        touched += end - start + 1

    ranges.sort()
    for previous, current in zip(ranges, ranges[1:]):
        if current[0] <= previous[1]:
            errors.append("{}edit ranges overlap".format(prefix))
    if touched > config.max_total_touched_lines:
        errors.append("{}total touched lines {} exceeds {}".format(
            prefix, touched, config.max_total_touched_lines
        ))
    if config.require_known_line_coverage and known_fault_lines:
        covered = any(
            start <= line <= end
            for start, end in ranges
            for line in known_fault_lines
        )
        if not covered:
            errors.append("{}no edit covers a known fault line".format(prefix))

    if not errors and apply_edits(source_text, edits) == source_text:
        errors.append("{}edits do not change the source".format(prefix))
    return errors


def validate_proposal(proposal, source_text, known_fault_lines, config):
    """Validate the earlier one-patch shape retained for utility compatibility."""
    errors = []
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    for field in ("diagnosis", "evidence_reasoning", "expected_effect", "edits"):
        if field not in proposal:
            errors.append("missing field: {}".format(field))
    errors.extend(_validate_edits(
        proposal.get("edits"), source_text, known_fault_lines, config
    ))
    return errors


def validate_batch_proposal(
    proposal, source_text, known_fault_lines, config, patch_count
):
    """Validate the shared envelope without rejecting valid sibling candidates."""
    errors = []
    if not isinstance(proposal, dict):
        return ["proposal must be an object"]
    for field in ("diagnosis", "evidence_reasoning", "uncertainty", "repair_candidates"):
        if field not in proposal:
            errors.append("missing field: {}".format(field))
    candidates = proposal.get("repair_candidates")
    if not isinstance(candidates, list):
        errors.append("repair_candidates must be an array")
        return errors
    if not candidates:
        errors.append("repair_candidates must contain at least one item")
    return errors


def validate_repair_candidate(
    candidate, source_text, known_fault_lines, config, prefix=""
):
    """Validate one candidate independently from the other candidates."""
    if not isinstance(candidate, dict):
        return ["{}must be an object".format(prefix)]
    errors = []
    for field in (
        "repair_intent", "assumption", "expected_effect",
        "preservation_constraints", "edits",
    ):
        if field not in candidate:
            errors.append("{}missing field: {}".format(prefix, field))
    errors.extend(_validate_edits(
        candidate.get("edits"), source_text, known_fault_lines, config, prefix
    ))
    return errors
