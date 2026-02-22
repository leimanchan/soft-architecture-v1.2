#!/usr/bin/env python3
"""Ensure each tool contracts.py defines ToolInput, ToolOutput, and run with strict shape."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Optional


def _has_dataclass_decorator(node: ast.ClassDef) -> bool:
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "dataclass":
            return True
        if isinstance(dec, ast.Attribute) and dec.attr == "dataclass":
            return True
    return False


def _annotation_name(node: Optional[ast.AST]) -> Optional[str]:
    if node is None:
        return None
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _run_signature_ok(node: ast.FunctionDef) -> Optional[str]:
    if len(node.args.args) != 1:
        return "run must accept exactly one argument"
    arg = node.args.args[0]
    arg_ann = _annotation_name(arg.annotation)
    if arg_ann != "ToolInput":
        return "run argument must be annotated as ToolInput"
    ret_ann = _annotation_name(node.returns)
    if ret_ann != "ToolOutput":
        return "run return annotation must be ToolOutput"
    return None


def _class_field_annotation(node: ast.ClassDef, field_name: str) -> Optional[ast.AST]:
    for stmt in node.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            if stmt.target.id == field_name:
                return stmt.annotation
    return None


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

        classes = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }
        functions = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }

        missing = {"ToolInput", "ToolOutput", "run"} - (set(classes) | set(functions))
        if missing:
            failures.append(f"{tool_dir.name}: missing {', '.join(sorted(missing))}")
            continue

        for cls_name in ("ToolInput", "ToolOutput"):
            cls = classes.get(cls_name)
            if not cls:
                continue
            if not _has_dataclass_decorator(cls):
                failures.append(f"{tool_dir.name}: {cls_name} must be a @dataclass")
                continue
            contracts_version_ann = _class_field_annotation(cls, "contracts_version")
            if contracts_version_ann is None:
                failures.append(
                    f"{tool_dir.name}: {cls_name} must define contracts_version: str"
                )
                continue
            if _annotation_name(contracts_version_ann) != "str":
                failures.append(
                    f"{tool_dir.name}: {cls_name}.contracts_version must be annotated as str"
                )

        run_fn = functions.get("run")
        if run_fn:
            err = _run_signature_ok(run_fn)
            if err:
                failures.append(f"{tool_dir.name}: {err}")

    if failures:
        print("Contracts check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Contracts check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
