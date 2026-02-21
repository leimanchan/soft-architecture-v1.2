#!/usr/bin/env python3
"""Register a tool in tools_registry.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: scripts/register_tool.py <tool_name> <description> [status]")
        return 1

    tool_name = sys.argv[1].strip()
    description = sys.argv[2].strip()
    status = sys.argv[3].strip() if len(sys.argv) > 3 else "active"

    root = Path(__file__).resolve().parents[1]
    registry_path = root / "tools_registry.json"

    if not registry_path.exists():
        print("tools_registry.json not found")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    tools = registry.get("tools", [])

    if any(tool.get("name") == tool_name for tool in tools):
        print(f"Tool already registered: {tool_name}")
        return 1

    tools.append({
        "name": tool_name,
        "description": description,
        "status": status,
        "contracts": f"core/{tool_name}/contracts.py",
        "origin": "new",
        "path": f"core/{tool_name}",
        "icon": "tool",
    })

    registry["tools"] = tools
    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Registered tool: {tool_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
