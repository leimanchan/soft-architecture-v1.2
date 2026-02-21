#!/usr/bin/env python3
"""Validate tools_registry.json entries."""

from __future__ import annotations

import ast
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
    seen_names = set()
    for tool in tools:
        if not isinstance(tool, dict):
            errors.append("Tool entry must be an object")
            continue
        name = tool.get("name")
        description = tool.get("description")
        status = tool.get("status")
        contracts = tool.get("contracts")
        path = tool.get("path")
        icon = tool.get("icon")
        tombstone = tool.get("tombstone")
        origin = tool.get("origin")
        if not name:
            errors.append("Tool missing 'name'")
        elif name in seen_names:
            errors.append(f"Duplicate tool name '{name}'")
        else:
            seen_names.add(name)
        if not description:
            errors.append(f"Tool '{name}' missing 'description'")
        elif isinstance(description, str) and description.strip().lower() == "todo":
            errors.append(f"Tool '{name}' description is TODO")
        if status not in {"active", "backburner", "deprecated"}:
            errors.append(f"Tool '{name}' invalid status '{status}'")
        if origin not in {"new", "migrated"}:
            errors.append(f"Tool '{name}' invalid origin '{origin}'")
        if not isinstance(path, str) or not path.strip():
            errors.append(f"Tool '{name}' missing 'path'")
        if not isinstance(icon, str) or not icon.strip():
            errors.append(f"Tool '{name}' missing 'icon'")
        if isinstance(path, str) and name and path != f"core/{name}":
            errors.append(f"Tool '{name}' path must be 'core/{name}', got '{path}'")
        if isinstance(path, str) and name:
            tool_root = root / path
            if not tool_root.exists() and not (status == "deprecated" and tombstone):
                errors.append(f"Tool '{name}' path not found: {path}")
        if not contracts:
            errors.append(f"Tool '{name}' missing 'contracts'")
        else:
            contracts_path = root / contracts
            if isinstance(path, str) and path.strip() and contracts != f"{path}/contracts.py":
                errors.append(
                    f"Tool '{name}' contracts must be '{path}/contracts.py', got '{contracts}'"
                )
            if not contracts_path.exists():
                if status == "deprecated" and tombstone:
                    continue
                errors.append(f"Tool '{name}' contracts path not found: {contracts}")
            else:
                try:
                    text = contracts_path.read_text(encoding="utf-8")
                    tree = ast.parse(text)
                    names = {
                        node.name
                        for node in ast.walk(tree)
                        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
                    }
                    missing = {"ToolInput", "ToolOutput", "run"} - names
                    if missing:
                        errors.append(
                            f"Tool '{name}' contracts missing {', '.join(sorted(missing))}"
                        )
                except Exception as exc:
                    errors.append(f"Tool '{name}' contracts parse failed: {exc}")

    if errors:
        print("tools_registry.json validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("tools_registry.json validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
