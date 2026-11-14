# Direct Program Repair with a Single LLM

The model receives:

- The source code to repair and a description of the program's functionality.
- Optional known faulty lines.
- Test cases permitted by the current experimental mode.
- MRs and violation information permitted by the current experimental mode.

The same LLM interprets the evidence, diagnoses the fault, and generates all candidate code edits in one structured response. The implementation performs only deterministic operations: validating edit ranges, applying edits, generating diffs, compiling, and running explicit checks.

## Experimental Modes

| Mode | Information provided to the LLM |
|---|---|
| `SOURCE_ONLY` | Source code, functional description, and optional faulty lines |
| `ORACLE` | The above information plus test cases with exact expected outputs |
| `MR` | Source code, test inputs and actual outputs, and MRs |
| `ORACLE_MR` | Combined Oracle and MR information |
| `AUTO` | Automatically selects a mode based on the input files |

`SOURCE_ONLY` removes test cases and MRs in the controller, rather than merely instructing the model to ignore them. It can therefore serve as a baseline for assessing whether MRs make an independent contribution to repair. `MR` mode also removes expected outputs inadvertently included in test cases and changes pass/fail labels to `unknown` to prevent oracle information leakage.

## Running the Implementation

First ensure that Ollama is running and the selected model is available. Then configure and run the example:

```powershell
python .\LLM\example_single_llm.py
```

The example sequentially executes three isolated scenarios:

```text
MR          -> testcase.json + mg_relation.json
Oracle      -> testcase_Oracle.json
MR_Oracle   -> testcase_Oracle.json + mg_relation.json
```

Results are written to `output_MR`, `output_Oracle`, and `output_MR_Oracle`, respectively. If a scenario fails, the error is recorded and the remaining scenarios continue, rather than terminating the entire experiment.

Alternatively, use the command-line interface:

```powershell
python .\LLM\run_repair.py .\code\DM\Mutant1.py `
  --function "Calculate the determinant of the input square matrix" `
  --mode MR `
  --tests .\code\DM\1\testcase.json `
  --mr .\code\DM\1\mg_relation.json `
  --fault-line 21 `
  --output-dir .\code\DM\1\LLM\output_MR
```

Python API example:

```python
from llm_repair import run_llm_repair

result = run_llm_repair(
    program_path="code/DM/Mutant1.py",
    program_function="Calculate the determinant of the input square matrix",
    test_executions="code/DM/1/testcase.json",
    mg_relation="code/DM/1/mg_relation.json",
    mode="MR",
    known_fault_line=21,
    patch_budget=5,
    model="deepcoder:14b",
    output_dir="code/DM/1/LLM/output_MR",
)
```

If `known_fault_line=None`, the model performs fault localization itself. Otherwise, this parameter accepts either an integer or a list of integers. By default, the model is allowed to modify causally related statements near the faulty line without requiring the patch to cover that line. Set `require_known_line_coverage=True` to enforce coverage.

## Multi-File C/C++ Projects

By default, the implementation infers compilation commands only for single-source-file programs. For multi-file projects, explicitly specify the project root and build command:

```python
result = run_llm_repair(
    program_path="code/PT/Mutants/printtokens_v0/print_tokens.c",
    project_root="code/PT/Mutants/printtokens_v0",
    program_function="A lexical analyzer implemented in C",
    mode="MR",
    test_executions=".../testcase.json",
    mg_relation=".../mg_relation.json",
    compile_command=[
        "gcc", "-std=c11", "print_tokens.c", "stream.c", "tokenizer.c",
        "-o", "{exe}",
    ],
    output_dir=".../LLM/output_MR",
)
```

Commands support the `{source}`, `{exe}`, and `{workdir}` placeholders. Runtime checks can also be supplied through `visible_checks`:

```python
visible_checks=[{
    "name": "example",
    "command": ["{exe}"],
    "stdin": "sample input\n",
    "timeout": 5,
}]
```

## Outputs

```text
output_MR/
├── 00_repair_input.json
├── 01_generation_attempts.json
├── 02_llm_analysis_and_repairs.json
├── 03_candidate_normalization.json
├── 04_patch_candidates.json
├── llm_repair_result.json
└── patches/P001/
    ├── proposal.json
    ├── patch.diff
    ├── patched_<original_filename>
    └── candidate.json
```

`patch_budget=5` requires a single LLM response to return five candidates based on a shared analysis of the evidence, rather than making five separate model calls. The model is instructed to explore different plausible repair directions without sacrificing correctness. When the fault and its correct repair are clear, the five candidates may share the same repair intent and code edits; the system does not force incorrect alternatives merely for diversity. Each candidate is applied independently to the original faulty program, without accumulating edits from earlier candidates.

Identical patches are still retained as five candidate records. To avoid redundant processing, subsequent identical patches reuse the compilation and explicit test results of the first occurrence. Their provenance is recorded through `duplicate_of` and `validation_reused_from`.

The default is `max_generation_retries=0`, so each scenario makes exactly one generation call. To regenerate a batch when the response contains errors in JSON formatting, candidate count, line numbers, or edit structure, explicitly set this parameter to a value greater than zero. A retry regenerates the entire candidate batch rather than making individual calls for each candidate.

`02_llm_analysis_and_repairs.json` stores the shared evidence analysis and all repair intents and candidate edits derived from it. Each `patches/Pxxx/proposal.json` combines the shared analysis with the corresponding candidate's repair intent to support individual inspection.

When `known_fault_line` is provided, each accepted model candidate must contain at least one edit covering that line; it may also modify other necessary related lines. The five candidates are validated individually, so errors in one candidate's line numbers, ranges, or anchors do not invalidate the others. If the response contains at least one valid candidate, invalid or missing slots are filled by copying the first valid candidate until there are five records. This is recorded in `03_candidate_normalization.json` and the candidate's `fallback_copy_of` field. No additional LLM call is made during this process.

The default context limit remains `num_ctx=32768`, which is typically sufficient for an ordinary source file of approximately 500 lines together with its evidence. The output limit, `num_predict`, has been increased to `8192` to accommodate five candidates in a single response. If `01_generation_attempts.json` reports `done_reason=length` or a `prompt_eval_count` close to the context limit, adjust `num_ctx` as supported by the local model rather than increasing GPU memory consumption unconditionally.
