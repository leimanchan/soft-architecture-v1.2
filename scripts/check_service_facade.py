#!/usr/bin/env python3
"""Ensure application/service.py is a facade only (imports/re-exports)."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_NODES = [
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.With,
]
if hasattr(ast, "Match"):
    FORBIDDEN_NODES.append(ast.Match)
FORBIDDEN_NODES = tuple(FORBIDDEN_NODES)


def _is_import_only_statement(node: ast.stmt) -> bool:
    return isinstance(node, (ast.Import, ast.ImportFrom))


def _is_dunder_all_assign(node: ast.stmt) -> bool:
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return False
    target = node.targets[0]
    return isinstance(target, ast.Name) and target.id == "__all__"


def _allowed_function(node: ast.FunctionDef) -> bool:
    if len(node.body) == 1 and isinstance(node.body[0], ast.Expr):
        expr = node.body[0]
        if isinstance(expr.value, ast.Constant) and isinstance(expr.value.value, str):
            return True
    if len(node.body) == 1 and isinstance(node.body[0], ast.Return):
        return True
    if len(node.body) == 2:
        first, second = node.body
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
            return isinstance(second, ast.Return)
    return False


def _check_service_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [f"{path}: syntax error"]

    failures: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            failures.append(f"{path}:{node.lineno}: control flow is not allowed in facade")
            break

    allowed = (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.Expr)
    for node in tree.body:
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                continue
            failures.append(f"{path}:{node.lineno}: only module docstring is allowed as bare expression")
            continue
        if isinstance(node, ast.Assign):
            if not _is_dunder_all_assign(node):
                failures.append(f"{path}:{node.lineno}: only __all__ assignment is allowed")
            continue
        if isinstance(node, ast.FunctionDef):
            if not _allowed_function(node):
                failures.append(f"{path}:{node.lineno}: facade functions must be thin passthroughs")
            continue
        if not isinstance(node, allowed):
            failures.append(f"{path}:{node.lineno}: unsupported node in service facade")

    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    failures: list[str] = []
    for tool_dir in core_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith("_"):
            continue
        service = tool_dir / "application" / "service.py"
        if not service.exists():
            continue
        failures.extend(_check_service_file(service))

    if failures:
        print("Service facade check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Service facade check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
