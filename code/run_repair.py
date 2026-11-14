import argparse
import json
import sys
from pathlib import Path

llm_root = Path(__file__).absolute().parent
sys.path.insert(0, str(llm_root))

from llm_repair import run_llm_repair


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Use one LLM stage to analyze evidence and directly repair a program."
    )
    parser.add_argument("program_path", help="faulty source file")
    parser.add_argument("--function", required=True, dest="program_function")
    parser.add_argument(
        "--mode",
        default="AUTO",
        choices=["AUTO", "SOURCE_ONLY", "ORACLE", "MR", "ORACLE_MR"],
    )
    parser.add_argument("--tests", dest="test_executions")
    parser.add_argument("--mr", dest="mg_relation")
    parser.add_argument("--fault-line", type=int, action="append", dest="fault_lines")
    parser.add_argument("--output-dir", default="llm_output")
    parser.add_argument("--project-root")
    parser.add_argument("--model", default="deepcoder:14b")
    parser.add_argument("--patch-budget", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def main():
    args = _parse_args()
    result = run_llm_repair(
        program_path=args.program_path,
        program_function=args.program_function,
        test_executions=args.test_executions,
        mg_relation=args.mg_relation,
        mode=args.mode,
        known_fault_line=args.fault_lines,
        output_dir=args.output_dir,
        project_root=args.project_root,
        model=args.model,
        patch_budget=args.patch_budget,
        temperature=args.temperature,
        seed=args.seed,
    )
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print(" Full results: {}".format(result["output_dir"]))


if __name__ == "__main__":
    main()
