#!/usr/bin/env python3
"""Compatibility wrapper for working-tree adapter sequencing checks."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def _python_cmd(root: Path, env: dict[str, str]) -> list[str]:
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
    cmd = _python_cmd(root, env) + ["scripts/check_adapter_sequence.py", "--scope", "working-tree"]
    result = subprocess.run(cmd, cwd=str(root), env=env)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
