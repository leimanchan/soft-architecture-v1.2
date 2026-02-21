#!/usr/bin/env python3
"""Ensure adapter imports are declared in requirements."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


def _parse_requirements(path: Path) -> set[str]:
    deps: set[str] = set()
    if not path.exists():
        return deps
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=@ ]", line, maxsplit=1)[0].strip().lower()
        if name:
            deps.add(name)
    return deps


def _stdlib_names() -> set[str]:
    try:
        return set(sys.stdlib_module_names)
    except Exception:
        return set()


def _collect_imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return set()

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    return imports


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    adapters_dir = root / "adapters"
    if not adapters_dir.exists():
        print("Adapters directory not found.")
        return 0

    declared = _parse_requirements(root / "requirements.txt") | _parse_requirements(
        root / "requirements-adapters.txt"
    )
    stdlib = _stdlib_names() | {
        "core",
        "adapters",
        "typing",
        "dataclasses",
        "pathlib",
        "json",
    }

    failures: list[str] = []
    for interface_dir in adapters_dir.iterdir():
        if not interface_dir.is_dir():
            continue
        for tool_dir in interface_dir.iterdir():
            if (
                not tool_dir.is_dir()
                or tool_dir.name in {"_base", "static", "templates"}
                or tool_dir.name.startswith(".")
            ):
                continue
            for path in tool_dir.rglob("*.py"):
                for imp in _collect_imports(path):
                    if imp in stdlib:
                        continue
                    if imp.lower() not in declared:
                        failures.append(
                            f"{tool_dir.name}: import '{imp}' in {path.relative_to(root)} not declared"
                        )

    if failures:
        print("Adapter dependency check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Adapter dependency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
