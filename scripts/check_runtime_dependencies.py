#!/usr/bin/env python3
"""Ensure adapters declare runtime dependencies."""

from __future__ import annotations

from pathlib import Path

MIN_LINES = 3
FORBIDDEN_MARKERS = {"todo", "tbd", "fixme"}


def _is_weak(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < MIN_LINES:
        return True
    if "install" not in text.lower():
        return True
    for line in lines:
        lower = line.lower()
        if any(marker in lower for marker in FORBIDDEN_MARKERS):
            return True
    return False


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    adapters_dir = root / "adapters"
    if not adapters_dir.exists():
        print("Adapters directory not found.")
        return 0

    failures: list[str] = []
    for interface_dir in adapters_dir.iterdir():
        if not interface_dir.is_dir():
            continue
        for tool_dir in interface_dir.iterdir():
            if (
                not tool_dir.is_dir()
                or tool_dir.name in {"_base", "static", "templates"}
                or tool_dir.name.startswith("__")
                or tool_dir.name.startswith(".")
            ):
                continue
            runtime_file = tool_dir / "RUNTIME_DEPENDENCIES.md"
            if not runtime_file.exists():
                failures.append(f"{tool_dir}: RUNTIME_DEPENDENCIES.md missing")
                continue
            text = runtime_file.read_text(encoding="utf-8")
            if _is_weak(text):
                failures.append(f"{tool_dir}: RUNTIME_DEPENDENCIES.md is too short or TODO")

    if failures:
        print("Runtime dependencies check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Runtime dependencies check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
