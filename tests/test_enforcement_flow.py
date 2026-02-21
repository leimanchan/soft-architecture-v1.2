import os
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: Path, env: dict | None = None) -> int:
    return subprocess.run(cmd, cwd=str(cwd), env=env, check=False).returncode


def test_enforcement_flow(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    temp_root = tmp_path / "repo"
    shutil.copytree(
        repo_root,
        temp_root,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache", "*.pyc"),
    )

    temp_test = temp_root / "tests" / "test_enforcement_flow.py"
    if temp_test.exists():
        temp_test.unlink()

    result = _run(
        [
            sys.executable,
            "scripts/new_tool_skeleton.py",
            "temp_tool",
            "--register",
            "--description",
            "Temporary tool",
        ],
        cwd=temp_root,
    )
    assert result == 0

    env = os.environ.copy()
    env["PYTHON_EXECUTABLE"] = sys.executable
    assert _run([sys.executable, "scripts/preflight_core.py"], cwd=temp_root, env=env) == 0

    decisions = temp_root / "core" / "temp_tool" / "DECISIONS.md"
    decisions.write_text("TODO\n", encoding="utf-8")

    assert _run(
        [sys.executable, "scripts/check_decisions_quality.py"],
        cwd=temp_root,
        env=env,
    ) != 0
