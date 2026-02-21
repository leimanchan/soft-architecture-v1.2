#!/usr/bin/env python3
"""Run pytest with coverage and enforce a minimum threshold."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_MIN = 50


def _python_cmd(root: Path) -> list[str]:
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return [str(venv_python)]
    return ["python3"]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    min_cov = int(env.get("MIN_COVERAGE", DEFAULT_MIN))
    cmd = _python_cmd(root) + [
        "-m",
        "pytest",
        "--cov=core",
        "--cov-report=term-missing",
        f"--cov-fail-under={min_cov}",
    ]
    result = subprocess.run(cmd, cwd=str(root), env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
