#!/usr/bin/env python3
"""Fail if core imports adapter/framework packages (AST-based)."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_IMPORTS = {
    "flask",
    "fastapi",
    "django",
    "click",
    "typer",
    "requests",
    "adapters",
}


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

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in FORBIDDEN_IMPORTS:
                    violations.append(f"{path}:{node.lineno}: forbidden import '{root}'")
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            root = node.module.split(".")[0]
            if root in FORBIDDEN_IMPORTS:
                violations.append(f"{path}:{node.lineno}: forbidden import '{root}'")
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
        print("Core purity check failed:")
        for v in violations:
            print(f"- {v}")
        return 1

    print("Core purity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
