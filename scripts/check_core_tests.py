#!/usr/bin/env python3
"""Ensure each registered tool has at least one decision test."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    registry_path = root / "tools_registry.json"

    if not core_dir.exists():
        print("core/ not found")
        return 1

    if not registry_path.exists():
        print("tools_registry.json not found")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    tools = registry.get("tools", [])
    registered = {t.get("name") for t in tools if t.get("status") != "deprecated"}

    core_tools = [d for d in core_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]

    if not registered:
        if core_tools:
            print("Core tools exist but registry is empty.")
            return 1
        print("No registered tools to check.")
        return 0

    failures = []
    for tool_name in sorted(registered):
        tool_dir = core_dir / tool_name
        if not tool_dir.exists():
            failures.append(f"{tool_name}: core folder missing")
            continue
        tests_dir = tool_dir / "tests"
        if not tests_dir.exists():
            failures.append(f"{tool_name}: tests/ missing")
            continue
        test_files = list(tests_dir.glob("test_*.py"))
        if not test_files:
            failures.append(f"{tool_name}: no test_*.py files in tests/")

    if failures:
        print("Core tests check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Core tests check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
