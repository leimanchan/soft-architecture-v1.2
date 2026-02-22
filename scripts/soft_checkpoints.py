#!/usr/bin/env python3
"""Check Soft Code workflow artifacts for a given tool."""

from __future__ import annotations

import sys
from pathlib import Path


def fail(msg: str) -> int:
    print(msg)
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        return fail("Usage: scripts/soft_checkpoints.py <tool_name>")

    tool = sys.argv[1].strip().lower().replace(" ", "_")
    if not tool:
        return fail("Tool name is required.")

    root = Path(__file__).resolve().parents[1]
    core = root / "core" / tool
    domain = core / "domain"
    app = core / "application"

    required = [
        core / "DECISIONS.md",
        domain / "models.py",
        domain / "specs.py",
        domain / "schema_checklist.md",
        core / "contracts.py",
        app / "orchestrator.py",
        app / "FILE_MAP.md",
        core / "examples" / "happy_path.json",
        core / "examples" / "invalid_path.json",
    ]

    missing = [path for path in required if not path.exists()]
    if missing:
        print("Missing required artifacts:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("All required artifacts exist.")
    print("Next: run scripts/check_core_purity.py and core tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
