#!/usr/bin/env python3
"""Run local-only checks (git hooks, env)."""

from __future__ import annotations

import subprocess
from pathlib import Path

CHECKS = [
    "scripts/check_hooks_installed.py",
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

    print("Preflight local passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
