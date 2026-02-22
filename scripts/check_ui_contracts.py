#!/usr/bin/env python3
"""Ensure Flask adapters include a minimal UI contract document."""

from __future__ import annotations

from pathlib import Path

REQUIRED_HEADINGS = [
    "## Routes",
    "## Request Payloads",
    "## Response Shapes",
    "## UI States",
    "## Core Contract Binding",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    flask_dir = root / "adapters" / "flask"
    if not flask_dir.exists():
        print("Flask adapters directory not found; skipping UI contract check.")
        return 0

    failures: list[str] = []
    for tool_dir in flask_dir.iterdir():
        if not tool_dir.is_dir() or tool_dir.name.startswith("_"):
            continue

        app_py = tool_dir / "app.py"
        if not app_py.exists():
            continue

        ui_contract = tool_dir / "UI_CONTRACT.md"
        if not ui_contract.exists():
            failures.append(f"{tool_dir.name}: missing adapters/flask/{tool_dir.name}/UI_CONTRACT.md")
            continue

        text = ui_contract.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                failures.append(f"{tool_dir.name}: UI_CONTRACT.md missing heading '{heading}'")

        if "`GET /`" not in text and "GET /" not in text:
            failures.append(f"{tool_dir.name}: UI_CONTRACT.md should document at least one concrete route")

    if failures:
        print("UI contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("UI contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
