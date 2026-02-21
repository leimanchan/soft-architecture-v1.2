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
            if isinstance(node.func, ast.Attribute) and node.func.attr == "raises":
                return True
    return False


def _test_calls_run(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "run":
                return True
            if isinstance(func, ast.Attribute) and func.attr == "run":
                return True
    return False


def _test_has_nontrivial_assert(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            # Reject trivial asserts like "assert True" or "assert __doc__"
            test = node.test
            if isinstance(test, ast.Constant) and test.value is True:
                continue
            if isinstance(test, ast.Attribute) and test.attr == "__doc__":
                continue
            if isinstance(test, ast.Name) and test.id == "__doc__":
                continue
            if isinstance(test, ast.Call):
                if isinstance(test.func, ast.Name) and test.func.id == "hasattr":
                    continue
            return True
    return False


def _test_case_count(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        return 0

    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            count += 1
    return count


def _test_has_negative_path(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == "raises":
                return True
    return False


def _test_file_is_meaningful(path: Path) -> bool:
    # Each test file should prove behavior (assertions) or validate failures.
    return _test_has_nontrivial_assert(path) or _test_has_negative_path(path)


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
            failures.append(f"{tool_name}: tests/ missing (add tests/test_*.py with real assertions)")
            continue
        test_files = list(tests_dir.glob("test_*.py"))
        if not test_files:
            failures.append(f"{tool_name}: no test_*.py files in tests/ (add at least one)")
            continue
        total_cases = sum(_test_case_count(p) for p in test_files)
        if not (len(test_files) >= 2 or total_cases >= 3):
            failures.append(
                f"{tool_name}: add tests (need >=2 test files or >=3 test cases)"
            )
            continue
        if not any(_test_has_asserts(p) for p in test_files):
            failures.append(f"{tool_name}: tests contain no asserts/raises (add real assertions)")
            continue
        if not any(_test_has_nontrivial_assert(p) for p in test_files):
            failures.append(f"{tool_name}: tests only contain trivial asserts (assert real behavior)")
            continue
        weak_files = [p.name for p in test_files if not _test_file_is_meaningful(p)]
        if weak_files:
            failures.append(
                f"{tool_name}: weak test files with no behavioral asserts/negative-path checks: "
                + ", ".join(sorted(weak_files))
            )
            continue
        if not any(_test_calls_run(p) for p in test_files):
            failures.append(f"{tool_name}: tests do not call run() (exercise contracts.run)")
            continue
        if not any(_test_has_negative_path(p) for p in test_files):
            failures.append(
                f"{tool_name}: add a negative-path test (e.g., pytest.raises on bad input)"
            )

    if failures:
        print("Core tests check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Core tests check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
