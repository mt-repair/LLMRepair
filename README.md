# LLMRepair: Code and Experimental Materials

This directory contains the single-stage LLM repair implementation, test evidence, and archived execution records for the paper *Metamorphic Testing for LLM-Based Program Repair: A Comparative Study*.

This document is based on the code and logs in the current directory. Regenerating candidate patches and reproducing the paper's human semantic assessments are separate steps. The repository should not currently be described as providing one-command reproduction of all results reported in the paper.

## 1. Directory Structure

```text
LLMRepair/
├── code/
│   ├── run_repair.py            # Command-line entry point for a single repair task
│   ├── example_single_llm.py    # Legacy batch example; requires adjustment before use
│   ├── requirements.txt        # requests>=2.28
│   ├── llm_repair/
│   │   ├── config.py           # Configuration structure and parameter validation
│   │   ├── prompts.py          # Prompts and structured-output constraints
│   │   ├── llm.py              # Ollama calls
│   │   ├── repairer.py         # Evidence selection, candidate generation, and processing
│   │   ├── patching.py         # Edit validation, application, and diff generation
│   │   ├── executor.py         # Workspaces, compilation, and optional explicit checks
│   │   └── io_utils.py         # JSON I/O and other utilities
│   └── tests/                 # Implementation tests, not evidence of patch correctness
└── result/
    ├── Qwen3/
    └── deepseek-r1/
        ├── TSQ/, SMM/, Tcas/, DM/, PT/, PT2/
        ├── *_Correct Repairs of Faulty Lines.json or *_Correct Repairs of Faulty Lines.json
        └── Program ID Used.txt
```

The `result` directory contains not only outputs but also subject programs, functional descriptions, MRs, and input evidence. Files such as `README` and `MR.md` in each program directory provide additional information about the subjects.

| Program | Functionality | Example variant directory |
|---|---|---|
| TSQ | Triangle area calculation | `TSQ/1/`; source at `TSQ/Mutant1.py` |
| SMM | Sparse matrix multiplication | `SMM/2/` |
| Tcas | Vertical collision-avoidance decisions | `Tcas/3/` |
| DM | Determinant calculation | `DM/1/` |
| PT | Lexical analysis | `PT/printtokens_v135/` |
| PT2 | Lexical analysis | `PT2/printtokens2_v19/` |

The directory also contains `Agent1`, `Agent2`, and other historical materials. For the single-stage implementation studied in this paper, use `LLM/output_*` under each variant. Agent1/Agent2 results must not be combined with these results in the analysis. The `scope` of `Qwen3_ structured analysis data .json` refers to earlier Agent1/Agent2 experiments; this file is not a set of aggregate labels for the current single-stage experiments under the three information conditions.

## 2. Information Conditions

The three conditions share the faulty source code, functional description, and known fault locations. Only the test evidence changes.

| Paper condition | API/CLI mode | Typical input files | Archived output directory |
|---|---|---|---|
| MT | `MR` | `testcase.json` + `mg_relation.json` | `LLM/output_MR` |
| Oracle | `ORACLE` | `testcase_Oracle.json` | `LLM/output_Oracle` |
| MT-Oracle / M&O | `ORACLE_MR` | `testcase_Oracle.json` + `mg_relation.json` | `LLM/output_MR_Oracle` |

The `MR` mode removes oracle fields such as `expected_output` from test records and changes any existing `test_status` to `unknown`. Consult `00_repair_input.json` for the actual input provided to the model, rather than relying only on the unprocessed test files. The current implementation removes the field instead of retaining the string `"missing"`.

MR files describe source tests, follow-up tests, input transformations, output relations, and relation statuses. Historical materials may contain original status codes such as `VMG`. Interpret these codes alongside the corresponding MR definitions; do not assume that every record uses the English status strings shown in the paper's examples.

The code also supports `SOURCE_ONLY` and `AUTO`, which are not among the three conditions reported in the paper.

## 3. Repair Workflow and Output Interpretation

1. Load the program and evidence, and select the information supplied to the model according to the mode.
2. Obtain a shared diagnosis and multiple candidate edits in one model call. The default candidate budget is 5, with 0 generation retries.
3. Validate edit line numbers, ranges, and coverage of known faulty lines. By default, each candidate may contain up to 3 edits affecting at most 20 lines.
4. Apply each candidate independently to the original faulty program, and save the modified source and diff.
5. Record compilation results and, if the caller supplies explicit checks, their execution results. The default workflow does not use these results for iterative repair.

Identical patches may be retained as multiple candidate records. If at least one valid candidate is available, invalid or missing candidate slots may be filled by copying a valid candidate without another model call. Inspect `fallback_copy_of`, `duplicate_of`, and `validation_reused_from`; five records do not necessarily represent five distinct, independently generated patches.

```text
output_MR/
├── 00_repair_input.json             # Actual input evidence, faulty lines, and generation constraints
├── 01_generation_attempts.json      # Model, parameters, call status, and parsing errors
├── 02_llm_analysis_and_repairs.json  # Shared diagnosis and candidate edits
├── 03_candidate_normalization.json  # Candidate validation and slot-filling records
├── 04_patch_candidates.json         # Candidates and processing results
├── llm_repair_result.json           # Complete run results and processing-status summary
└── patches/P001/
    ├── proposal.json
    ├── candidate.json
    ├── patch.diff
    └── patched_<source_filename>
```

`compile_passed` indicates only that a build or syntax check passed. `generation_failed` indicates a failure during candidate generation or parsing. Neither status replaces the human semantic assessments used in the paper.

## 4. Environment and Single-Task Execution

Python, `requests`, and an Ollama service hosting the selected model are required. The default service address is `http://localhost:11434`. C/C++ programs also require the corresponding compiler; projects with multiple source files require a build command appropriate for those files.

Run the following commands from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\code\requirements.txt
```

Ensure that Ollama is running and that the model corresponding to the archived run is installed. The following TSQ-1 example uses the Qwen3 parameters recorded in the logs and writes results to a new directory to avoid overwriting archived records:

```powershell
.\.venv\Scripts\python.exe .\code\run_repair.py `
  .\result\Qwen3\TSQ\Mutant1.py `
  --function "Calculate the area of a triangle given three side lengths." `
  --mode MR `
  --tests .\result\Qwen3\TSQ\1\testcase.json `
  --mr .\result\Qwen3\TSQ\1\mg_relation.json `
  --fault-line 21 `
  --model "Qwen3:14b" `
  --temperature 0.09 `
  --seed 0 `
  --patch-budget 5 `
  --output-dir .\reruns\Qwen3\TSQ\1\output_MR
```

This command illustrates how to invoke the implementation. Its functional description is abbreviated, so it is not an exact reproduction of the original experimental input. To rerun an archived experiment faithfully, use the complete `program_function` and `known_fault_lines` from `00_repair_input.json`, and obtain the model configuration from that run's `01_generation_attempts.json`.

For the Oracle condition, use `--mode ORACLE` with `testcase_Oracle.json` and omit `--mr`. For the combined condition, use `--mode ORACLE_MR` with both the Oracle test file and the MR file. Use a separate output directory for each condition.

The defaults in `run_repair.py` are `deepcoder:14b` for the model and 0.05 for temperature. Therefore, specify these parameters explicitly when running the models studied in the paper. `example_single_llm.py` still uses an older directory layout and contains a mismatch between variant identifiers and faulty lines through `mutant = i` and `line[i-1]`. It is not recommended as a ready-to-run entry point for the complete experiment.

## 5. Archived Configurations and Reproduction Scope

A scan of the direct experiment directories matching `result/<model>/<program>/<variant>/LLM/output_*/01_generation_attempts.json` yielded the following counts:

| Model directory | Run logs | temperature=0.09 | temperature=0.05 |
|---|---:|---:|---:|
| Qwen3 | 201 | 183 | 18 |
| deepseek-r1 | 197 | 181 | 16 |

## 6. Semantic Evaluation and Paper Results

The paper uses LLM-assisted assessment followed by human verification to determine whether the target statements conform to the reference semantics. A run is counted as a confirmed success if at least one candidate conforms to those semantics. This does not imply that the complete patch passes an independent test suite.

Files such as `*_ faulty-line repair results .json` under each model directory record reference edits, including fields such as `version`, `fault_line`, and `repaired_code`.

To review a result, examine the following together:

1. The original variant, functional description, and reference edit.
2. The actual test evidence provided in `00_repair_input.json`.
3. The model diagnosis, `proposal.json`, and `patch.diff`.
4. The human semantic judgment and its rationale.

Reproducing the success rates and Venn diagrams requires a consistent final sample list and final judgment table.

Calling the LLM again may produce different patches because of differences in the execution environment or model version.

## 7. Verification Scope of This Document

Complete execution and reproduction of the paper's results require the environment and materials described above.
