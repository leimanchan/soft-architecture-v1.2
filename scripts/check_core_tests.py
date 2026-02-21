#!/usr/bin/env python3
"""Ensure each tool has meaningful tests and registry matches core."""

from __future__ import annotations

import ast
import json
from pathlib import Path


def _test_has_asserts(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            return True
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "raises":
                    return True
    return False


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
    registered = {t.get("name") for t in tools if t.get("status") != "deprecated" and t.get("name")}

    core_tools = [d for d in core_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]
    core_names = {d.name for d in core_tools}

    if not registered:
        if core_tools:
            print("Core tools exist but registry is empty.")
            return 1
        print("No registered tools to check.")
        return 0

    failures = []

    unregistered = core_names - registered
    if unregistered:
        failures.append(f"Unregistered core tools: {', '.join(sorted(unregistered))}")

    missing_core = registered - core_names
    if missing_core:
        failures.append(f"Registry tools missing in core/: {', '.join(sorted(missing_core))}")

    for tool_name in sorted(registered & core_names):
        tool_dir = core_dir / tool_name
        tests_dir = tool_dir / "tests"
        if not tests_dir.exists():
            failures.append(f"{tool_name}: tests/ missing")
            continue
        test_files = list(tests_dir.glob("test_*.py"))
        if not test_files:
            failures.append(f"{tool_name}: no test_*.py files in tests/")
            continue
        if not any(_test_has_asserts(p) for p in test_files):
            failures.append(f"{tool_name}: tests contain no asserts/raises")

    if failures:
        print("Core tests check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Core tests check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
