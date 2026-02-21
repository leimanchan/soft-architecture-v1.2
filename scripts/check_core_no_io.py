#!/usr/bin/env python3
"""Fail if core contains filesystem or process side effects (AST-based)."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_MODULES = {
    "os",
    "pathlib",
    "tempfile",
    "subprocess",
    "socket",
    "shutil",
    "glob",
    "ftplib",
    "imaplib",
    "poplib",
    "smtplib",
    "telnetlib",
    "urllib",
    "http",
}

FORBIDDEN_FUNCS = {
    "open",
    "system",
    "popen",
    "__import__",
}

FORBIDDEN_METHODS = {
    "open",
    "read_text",
    "write_text",
    "mkdir",
    "rglob",
    "glob",
    "iterdir",
    "unlink",
    "rename",
    "replace",
    "rmdir",
    "chmod",
    "touch",
    "exists",
    "stat",
    "lstat",
    "walk",
    "listdir",
    "remove",
    "makedirs",
    "mkdtemp",
    "mkstemp",
    "getenv",
    "import_module",
}


def _import_map(tree: ast.AST) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mapping[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            for alias in node.names:
                mapping[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    return mapping


def _root_name(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    if isinstance(current, ast.Name):
        return current.id
    return None


def scan_file(path: Path) -> list[str]:
    violations = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return violations
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return violations

    imports = _import_map(tree)

    # Fail on forbidden imports directly
    for name, module in imports.items():
        if module.split(".")[0] in FORBIDDEN_MODULES:
            violations.append(f"{path}: forbidden import '{module}'")

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                name = func.id
                if name in FORBIDDEN_FUNCS:
                    violations.append(f"{path}:{node.lineno}: forbidden IO call '{name}'")
                if name in imports:
                    root_module = imports[name].split(".")[0]
                    if root_module in FORBIDDEN_MODULES:
                        violations.append(f"{path}:{node.lineno}: forbidden IO call '{imports[name]}'")
            elif isinstance(func, ast.Attribute):
                root = _root_name(func)
                attr = func.attr
                if (
                    isinstance(func.value, ast.Name)
                    and func.value.id == "importlib"
                    and attr == "import_module"
                ):
                    violations.append(f"{path}:{node.lineno}: forbidden dynamic import 'importlib.import_module'")
                if root in imports:
                    root_module = imports[root].split(".")[0]
                    if root_module in FORBIDDEN_MODULES:
                        violations.append(f"{path}:{node.lineno}: forbidden IO call '{root_module}'")
                    if attr in FORBIDDEN_METHODS:
                        violations.append(f"{path}:{node.lineno}: forbidden IO method '{attr}' on '{root_module}'")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    core_dir = root / "core"
    if not core_dir.exists():
        print("core/ not found")
        return 1

    violations: list[str] = []
    for path in core_dir.rglob("*.py"):
        violations.extend(scan_file(path))

    if violations:
        print("Core IO purity check failed:")
        for v in violations:
            print(f"- {v}")
        return 1

    print("Core IO purity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
