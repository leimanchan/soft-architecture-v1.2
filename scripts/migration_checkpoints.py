#!/usr/bin/env python3
"""Check migration artifacts for a given tool."""

from __future__ import annotations

import sys
from pathlib import Path


def fail(msg: str) -> int:
    print(msg)
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        return fail("Usage: scripts/migration_checkpoints.py <tool_name>")

    tool = sys.argv[1].strip().lower().replace(" ", "_")
    if not tool:
        return fail("Tool name is required.")

    root = Path(__file__).resolve().parents[1]
    core = root / "core" / tool
    domain = core / "domain"
    app = core / "application"
    contracts = core / "contracts.py"

    required = [
        core / "DECISIONS.md",
        domain / "models.py",
        domain / "specs.py",
        domain / "schema_checklist.md",
        app / "service.py",
        app / "orchestrator.py",
        contracts,
        core / "examples" / "happy_path.json",
        core / "examples" / "invalid_path.json",
        core / "MIGRATION_MAP.md",
    ]

    missing = [path for path in required if not path.exists()]
    if missing:
        print("Missing required artifacts:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("Migration checkpoints passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
