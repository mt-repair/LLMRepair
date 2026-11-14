import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

from .io_utils import tail_text


def _format_command(command, variables):
    if command is None:
        return None
    if isinstance(command, (list, tuple)):
        return [str(item).format(**variables) for item in command]
    return shlex.split(str(command).format(**variables), posix=(os.name != "nt"))


def _run(command, cwd, timeout, stdin_text=None):
    started = time.monotonic()
    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            input=stdin_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            shell=False,
        )
        return {
            "attempted": True,
            "success": proc.returncode == 0,
            "return_code": proc.returncode,
            "timed_out": False,
            "stdout_tail": tail_text(proc.stdout),
            "stderr_tail": tail_text(proc.stderr),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": [str(item) for item in command],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "attempted": True,
            "success": False,
            "return_code": None,
            "timed_out": True,
            "stdout_tail": tail_text(exc.stdout),
            "stderr_tail": tail_text(exc.stderr),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": [str(item) for item in command],
        }
    except OSError as exc:
        return {
            "attempted": True,
            "success": False,
            "return_code": None,
            "timed_out": False,
            "stdout_tail": "",
            "stderr_tail": str(exc),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": [str(item) for item in command],
        }


def prepare_workspace(program_path, project_root, candidate_dir, output_dir):
    program_path = Path(program_path).absolute()
    project_root = Path(project_root).absolute()
    relative_source = program_path.relative_to(project_root)
    workspace = Path(candidate_dir).absolute() / "workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    output_dir = Path(output_dir).absolute()

    def ignore(path, names):
        ignored = {name for name in names if name in {
            ".git", "__pycache__", ".pytest_cache", ".idea", ".vscode"
        }}
        current = Path(path).absolute()
        for name in names:
            candidate = (current / name).absolute()
            try:
                candidate.relative_to(output_dir)
                ignored.add(name)
            except ValueError:
                pass
        return ignored

    shutil.copytree(project_root, workspace, ignore=ignore)
    copied_source = workspace / relative_source
    if not copied_source.is_file():
        raise RuntimeError("source was not copied into validation workspace")
    return workspace, copied_source


def validate_candidate(
    patched_source,
    workspace,
    compile_command,
    visible_checks,
    compile_timeout,
    check_timeout,
):
    exe = Path(workspace) / ("llm_candidate.exe" if os.name == "nt" else "llm_candidate")
    variables = {
        "source": str(patched_source),
        "exe": str(exe),
        "workdir": str(workspace),
    }
    command = _format_command(compile_command, variables)
    if command is None:
        suffix = patched_source.suffix.lower()
        if suffix == ".py":
            command = [sys.executable, "-m", "py_compile", str(patched_source)]
        elif suffix == ".c" and (shutil.which("gcc") or shutil.which("clang")):
            command = [shutil.which("gcc") or shutil.which("clang"), "-std=c11", str(patched_source), "-o", str(exe)]
        elif suffix in {".cc", ".cpp", ".cxx"} and (shutil.which("g++") or shutil.which("clang++")):
            command = [shutil.which("g++") or shutil.which("clang++"), "-std=c++17", str(patched_source), "-o", str(exe)]

    if command is None:
        compile_result = {
            "attempted": False,
            "success": None,
            "stderr_tail": "No compile command could be inferred.",
            "command": [],
            "executable_path": None,
        }
    else:
        compile_result = _run(command, workspace, compile_timeout)
        compile_result["executable_path"] = str(exe) if exe.exists() else None

    checks = []
    if compile_result.get("success") is not False:
        for index, check in enumerate(visible_checks or [], 1):
            if not isinstance(check, dict):
                check = {"command": check}
            check_command = _format_command(check.get("command"), variables)
            if not check_command:
                checks.append({
                    "name": check.get("name", "check_{}".format(index)),
                    "attempted": False,
                    "success": None,
                    "stderr_tail": "empty command",
                })
                continue
            result = _run(
                check_command,
                workspace,
                int(check.get("timeout", check_timeout)),
                check.get("stdin", ""),
            )
            result["name"] = check.get("name", "check_{}".format(index))
            checks.append(result)
    return {"compile": compile_result, "visible_checks": checks}
