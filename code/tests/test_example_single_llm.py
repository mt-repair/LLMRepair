import importlib.util
from pathlib import Path


def _load_example():
    path = Path(__file__).parents[1] / "example_single_llm.py"
    spec = importlib.util.spec_from_file_location("example_single_llm_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_example_runs_three_isolated_scenarios(tmp_path, monkeypatch):
    module = _load_example()
    program_dir = tmp_path / "code" / "DM"
    case_dir = program_dir / "1"
    case_dir.mkdir(parents=True)
    (program_dir / "Mutant1.py").write_text("x = 1\n", encoding="utf-8")
    (case_dir / "testcase.json").write_text("[]", encoding="utf-8")
    (case_dir / "testcase_Oracle.json").write_text("[]", encoding="utf-8")
    (case_dir / "mg_relation.json").write_text("[]", encoding="utf-8")

    calls = []

    def fake_run(**kwargs):
        calls.append(kwargs)
        return {"summary": {}, "patch_candidates": []}

    monkeypatch.setattr(module, "msbf_root", tmp_path)
    monkeypatch.setattr(module, "run_llm_repair", fake_run)
    module.main()

    assert [call["mode"] for call in calls] == ["MR", "ORACLE", "ORACLE_MR"]
    assert calls[0]["test_executions"].name == "testcase.json"
    assert calls[0]["mg_relation"].name == "mg_relation.json"
    assert calls[1]["test_executions"].name == "testcase_Oracle.json"
    assert calls[1]["mg_relation"] is None
    assert calls[2]["test_executions"].name == "testcase_Oracle.json"
    assert calls[2]["mg_relation"].name == "mg_relation.json"
    assert [call["output_dir"].name for call in calls] == [
        "output_MR", "output_Oracle", "output_MR_Oracle"
    ]
