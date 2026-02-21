#!/usr/bin/env python3
"""Run core repository checks (CI-safe)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

CHECKS = [
    "scripts/check_core_purity.py",
    "scripts/check_core_no_io.py",
    "scripts/check_decisions_quality.py",
    "scripts/check_core_tests.py",
    "scripts/check_contracts.py",
    "scripts/check_test_coverage.py",
    "scripts/check_agent_docs.py",
    "scripts/check_tools_registry.py",
    "scripts/check_adapter_no_inline_styles.py",
    "scripts/check_adapter_uses_base.py",
    "scripts/check_adapter_sequence.py",
    "scripts/check_orchestrator_dumb.py",
]


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
    python_cmd = _python_cmd(root, env)

    for check in CHECKS:
        path = root / check
        if not path.exists():
            print(f"Missing check: {check}")
            return 1
        result = subprocess.run(python_cmd + [str(path)], cwd=str(root), env=env)
        if result.returncode != 0:
            return result.returncode

    print("Preflight core passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
