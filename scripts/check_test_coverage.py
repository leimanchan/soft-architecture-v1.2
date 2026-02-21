#!/usr/bin/env python3
"""Run pytest with coverage and enforce a minimum threshold."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

STAGE_MINIMUMS = {
    "stage1": 65,
    "stage2": 75,
}
DEFAULT_STAGE = "stage1"


def _python_cmd(root: Path, env: dict) -> list[str]:
    override = env.get("PYTHON_EXECUTABLE")
    if override:
        return [override]
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return [str(venv_python)]
    return ["python3"]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    if "MIN_COVERAGE" in env:
        min_cov = int(env["MIN_COVERAGE"])
    else:
        stage = env.get("COVERAGE_STAGE", DEFAULT_STAGE).strip().lower()
        if stage not in STAGE_MINIMUMS:
            allowed = ", ".join(sorted(STAGE_MINIMUMS))
            print(f"Invalid COVERAGE_STAGE '{stage}'. Expected one of: {allowed}")
            return 1
        min_cov = STAGE_MINIMUMS[stage]
        print(f"Coverage gate: {stage} (minimum {min_cov}%).")
    cmd = _python_cmd(root, env) + [
        "-m",
        "pytest",
        "--import-mode=importlib",
        "--cov=core",
        "--cov-report=term-missing",
        f"--cov-fail-under={min_cov}",
    ]
    result = subprocess.run(cmd, cwd=str(root), env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
