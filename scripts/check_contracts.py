#!/usr/bin/env python3
"""Ensure each tool contracts.py defines ToolInput, ToolOutput, and run."""

from __future__ import annotations

import ast
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    failures = []
    for tool_dir in core_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith("_"):
            continue
        contracts = tool_dir / "contracts.py"
        if not contracts.exists():
            failures.append(f"{tool_dir.name}: contracts.py missing")
            continue
        text = contracts.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            failures.append(f"{tool_dir.name}: contracts.py syntax error")
            continue

        names = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        missing = {"ToolInput", "ToolOutput", "run"} - names
        if missing:
            failures.append(f"{tool_dir.name}: missing {', '.join(sorted(missing))}")

    if failures:
        print("Contracts check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Contracts check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
