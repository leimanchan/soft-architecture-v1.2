#!/usr/bin/env python3
"""Ensure migrated tools include a migration mapping artifact."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry_path = root / "tools_registry.json"

    if not registry_path.exists():
        print("tools_registry.json not found")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    tools = registry.get("tools", [])

    failures: list[str] = []
    for tool in tools:
        if tool.get("origin") != "migrated":
            continue
        name = tool.get("name")
        if not name:
            continue
        path = root / "core" / name / "MIGRATION_MAP.md"
        if not path.exists():
            failures.append(f"{name}: MIGRATION_MAP.md missing")
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text or "todo" in text.lower():
            failures.append(f"{name}: MIGRATION_MAP.md is empty or TODO")

    if failures:
        print("Migration map check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Migration map check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
