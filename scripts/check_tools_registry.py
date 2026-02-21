#!/usr/bin/env python3
"""Validate tools_registry.json entries."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry_path = root / "tools_registry.json"

    if not registry_path.exists():
        print("tools_registry.json not found")
        return 1

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Failed to parse tools_registry.json: {exc}")
        return 1

    tools = registry.get("tools")
    if not isinstance(tools, list):
        print("Registry 'tools' must be a list")
        return 1

    errors = []
    for tool in tools:
        if not isinstance(tool, dict):
            errors.append("Tool entry must be an object")
            continue
        name = tool.get("name")
        description = tool.get("description")
        status = tool.get("status")
        contracts = tool.get("contracts")
        if not name:
            errors.append("Tool missing 'name'")
        if not description:
            errors.append(f"Tool '{name}' missing 'description'")
        elif isinstance(description, str) and description.strip().lower() == "todo":
            errors.append(f"Tool '{name}' description is TODO")
        if status not in {"active", "backburner", "deprecated"}:
            errors.append(f"Tool '{name}' invalid status '{status}'")
        if not contracts:
            errors.append(f"Tool '{name}' missing 'contracts'")
        else:
            if not (root / contracts).exists():
                errors.append(f"Tool '{name}' contracts path not found: {contracts}")

    if errors:
        print("tools_registry.json validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("tools_registry.json validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
