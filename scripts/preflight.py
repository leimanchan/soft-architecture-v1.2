#!/usr/bin/env python3
"""Run all preflight checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECKS = [
    "scripts/check_core_purity.py",
    "scripts/check_core_no_io.py",
    "scripts/check_core_tests.py",
    "scripts/check_agent_docs.py",
    "scripts/check_tools_registry.py",
    "scripts/check_adapter_no_inline_styles.py",
    "scripts/check_adapter_uses_base.py",
    "scripts/check_adapter_after_core.py",
    "scripts/check_orchestrator_dumb.py",
    "scripts/guard_adapters.py",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    for check in CHECKS:
        path = root / check
        if not path.exists():
            print(f"Missing check: {check}")
            return 1
        result = subprocess.run(["python3", str(path)], cwd=str(root))
        if result.returncode != 0:
            return result.returncode

    print("Preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
