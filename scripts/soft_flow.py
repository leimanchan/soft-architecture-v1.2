#!/usr/bin/env python3
"""Print the deterministic Soft Code workflow steps."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs" / "soft"

    steps = [
        "WORKFLOW.md",
        "01_decision_list.md",
        "02_data_shapes.md",
        "03_decision_functions.md",
        "04_orchestrator.md",
        "05_adapters_and_io.md",
        "06_verification.md",
    ]

    print("Soft Code Workflow")
    print("=" * 20)
    for step in steps:
        path = docs / step
        print(f"- {path}")

    print("\nUsage: open each doc in order and follow the outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
