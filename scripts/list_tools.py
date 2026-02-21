#!/usr/bin/env python3
"""List tools from tools_registry.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    status_filter = sys.argv[1].strip() if len(sys.argv) > 1 else None

    root = Path(__file__).resolve().parents[1]
    registry_path = root / "tools_registry.json"

    if not registry_path.exists():
        print("tools_registry.json not found")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    tools = registry.get("tools", [])

    if status_filter:
        tools = [t for t in tools if t.get("status") == status_filter]

    for tool in tools:
        name = tool.get("name", "")
        status = tool.get("status", "")
        description = tool.get("description", "")
        print(f"- {name} [{status}] {description}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
