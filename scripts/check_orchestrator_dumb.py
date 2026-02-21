#!/usr/bin/env python3
"""Enforce dumb orchestrator: no branching/loops and small size."""

from __future__ import annotations

import ast
from pathlib import Path

MAX_LINES = 60

FORBIDDEN_NODES = [ast.If, ast.For, ast.While, ast.Try, ast.With]
if hasattr(ast, "Match"):
    FORBIDDEN_NODES.append(ast.Match)
FORBIDDEN_NODES = tuple(FORBIDDEN_NODES)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    violations = []
    for tool_dir in core_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith("_"):
            continue
        orch = tool_dir / "application" / "orchestrator.py"
        if not orch.exists():
            continue
        text = orch.read_text(encoding="utf-8")
        if len(text.splitlines()) > MAX_LINES:
            violations.append(f"{orch}: too long (>{MAX_LINES} lines)")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, FORBIDDEN_NODES):
                violations.append(f"{orch}:{node.lineno}: branching/loop not allowed")
                break

    if violations:
        print("Orchestrator check failed:")
        for v in violations:
            print(f"- {v}")
        return 1

    print("Orchestrator check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
