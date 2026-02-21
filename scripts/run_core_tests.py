#!/usr/bin/env python3
"""Run core tests via pytest."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def _python_cmd(root: Path) -> list[str]:
    venv_python = root / ".venv" / "bin" / "python"
    if venv_python.exists():
        return [str(venv_python)]
    return ["python3"]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    cmd = _python_cmd(root) + ["-m", "pytest", "core"]
    result = subprocess.run(cmd, cwd=str(root), env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
