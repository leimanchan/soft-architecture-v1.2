#!/usr/bin/env python3
"""Ensure example payloads exist and are valid JSON."""

from __future__ import annotations

import json
from pathlib import Path


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
        examples_dir = tool_dir / "examples"
        happy = examples_dir / "happy_path.json"
        invalid = examples_dir / "invalid_path.json"
        for path in [happy, invalid]:
            if not path.exists():
                failures.append(f"{tool_dir.name}: missing {path}")
                continue
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                failures.append(f"{tool_dir.name}: invalid JSON in {path} ({exc})")

    if failures:
        print("Examples check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Examples check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
