#!/usr/bin/env python3
"""Fail if core imports adapter/framework packages."""

from __future__ import annotations

import sys
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

    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("import ") or stripped.startswith("from "):
            for forbidden in FORBIDDEN_IMPORTS:
                if f"import {forbidden}" in stripped or f"from {forbidden}" in stripped:
                    violations.append(f"{path}:{i}: forbidden import '{forbidden}'")
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
