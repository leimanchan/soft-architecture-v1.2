#!/usr/bin/env python3
"""Fail if DECISIONS.md is missing or too weak."""

from __future__ import annotations

from pathlib import Path

MIN_LINES = 5
FORBIDDEN_MARKERS = {"todo", "tbd", "fixme"}


def _is_weak(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < MIN_LINES:
        return True
    for line in lines:
        lower = line.lower()
        if any(marker in lower for marker in FORBIDDEN_MARKERS):
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
        decisions = tool_dir / "DECISIONS.md"
        if not decisions.exists():
            failures.append(f"{tool_dir.name}: DECISIONS.md missing")
            continue
        text = decisions.read_text(encoding="utf-8")
        if _is_weak(text):
            failures.append(
                f"{tool_dir.name}: DECISIONS.md too short or contains placeholders (add real decisions)"
            )

    if failures:
        print("Decisions quality check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Decisions quality check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
