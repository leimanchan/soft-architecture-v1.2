#!/usr/bin/env python3
"""Ensure schema_checklist.md exists and is non-trivial for each tool."""

from __future__ import annotations

from pathlib import Path

MIN_LINES = 4
FORBIDDEN_MARKERS = {"todo", "tbd", "fixme"}


def _is_weak(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < MIN_LINES:
        return True
    for line in lines:
        lower = line.lower()
        if any(marker in lower for marker in FORBIDDEN_MARKERS):
            return True
    if "required fields" not in text.lower():
        return True
    if "contracts_version" not in text.lower():
        return True
    return False


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
        path = tool_dir / "domain" / "schema_checklist.md"
        if not path.exists():
            failures.append(f"{tool_dir.name}: domain/schema_checklist.md missing")
            continue
        text = path.read_text(encoding="utf-8")
        if _is_weak(text):
            failures.append(f"{tool_dir.name}: schema_checklist.md is too short or TODO")

    if failures:
        print("Schema checklist check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Schema checklist check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
