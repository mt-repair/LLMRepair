import sys
from pathlib import Path

llm_root = Path(__file__).absolute().parent
msbf_root = llm_root.parent
sys.path.insert(0, str(llm_root))

from llm_repair import run_llm_repair


# index = [1, 2, 3, 4, 5]
# line = [21, 24, 21, 21, 27]
# program = "DM"


# index = [2, 3, 4, 5, 6]
# line = [43, 43, 48, 47, 47]
# program = "SMM"

index = [1, 2, 3, 4, 5, 6]
line = [21, 26, 29, 34, 40, 42]
program = "TSQ"

# index = [2, 3, 4, 7, 18, 20]
# line = [16, 59, 63, 24, 16, 16]
# program = "Tcas"

model = "deepseek-r1:14b"
# model = "Qwen3:14b"

for i in range(len(index)):
    #  Modify here to select the subject program; the three evidence scenarios will run independently in sequence. 
    mutant = i
    known_fault_line = line[i-1]
    patch_budget = 5
    
    temperature = 0.05
    max_generation_retries = 0  #  Each scenario is strictly called only once LLM Generate Batch Patches 
    require_known_line_coverage = True  #  Each valid patch must cover a known faulty line. 
    program_function = '''
        Program name: Trisquare
        Function: Calculate the area of a triangle given three side lengths.
        Input: argv, a list containing three numeric side lengths [a, b, c].
        Output: returns a tuple (area, symbol). symbol is always 0.
        Behavior:
        1. If any side ≤ 0 or triangle‑inequality is violated, print "Not a triangle" and return (0, 0).
        2. For valid triangle sides: classify triangle as acute, right‑angled or obtuse.
        Use corresponding formulas to compute area for isosceles and scalene cases.
 '''

    #  scenario name, mode, testcase Document, whether to use MR。
    scenarios = (
        ("MR", "MR", "testcase.json", True),
        ("Oracle", "ORACLE", "testcase_Oracle.json", False),
        ("MR_Oracle", "ORACLE_MR", "testcase_Oracle.json", True),
    )



    program_dir = msbf_root / "code" / program
    case_dir = program_dir / str(mutant)
    program_path = program_dir / "Mutant{}.py".format(mutant)

    mr_path = case_dir / "mg_relation.json"
    succeeded = []
    failed = []

    for scenario_name, mode, testcase_name, use_mr in scenarios:
        test_path = case_dir / testcase_name
        output_dir = case_dir / "LLM" / "output_{}".format(scenario_name)
        print(
            "== Start ===========Mutant{} / {}==========================".format(
                mutant, scenario_name
            )
        )
        try:
            result = run_llm_repair(
                program_path=program_path,
                program_function=program_function,
                test_executions=test_path,
                mg_relation=(mr_path if use_mr else None),
                mode=mode,
                known_fault_line=known_fault_line,
                patch_budget=patch_budget,
                model=model,
                temperature=temperature,
                max_generation_retries=max_generation_retries,
                require_known_line_coverage=require_known_line_coverage,
                output_dir=output_dir,
            )
            print(" Completed: ", result["summary"])
            for candidate in result["patch_candidates"]:
                print(candidate["patch_id"], candidate["status"])
            succeeded.append(scenario_name)
        except Exception as exc:
            print(
                "{}  Execution failed: {}: {}".format(
                    scenario_name, type(exc).__name__, exc
                ),
                file=sys.stderr,
            )
            failed.append((scenario_name, "{}: {}".format(type(exc).__name__, exc)))
        print(
            "== End ===========Mutant{} / {}==========================".format(
                mutant, scenario_name
            )
        )

    print(" Three-scenario operation completed: Successful  {}  failed  {}".format(len(succeeded), len(failed)))
    if succeeded:
        print(" Success Scenario: {}".format(succeeded))
    if failed:
        print(" Failure Scenario: {}".format(failed), file=sys.stderr)


