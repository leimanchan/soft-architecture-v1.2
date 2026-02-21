#!/usr/bin/env python3
"""Create a new tool skeleton following the core + adapter structure."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: scripts/new_tool_skeleton.py <tool_name> [--register --description \"...\"]")
        return 1

    tool_name = sys.argv[1].strip().lower().replace(" ", "_")
    if not tool_name:
        print("Tool name is required.")
        return 1

    args = sys.argv[2:]
    register = "--register" in args
    description = None
    if "--description" in args:
        idx = args.index("--description")
        if idx + 1 < len(args):
            description = args[idx + 1].strip()

    root = Path(__file__).resolve().parents[1]

    core_dir = root / "core" / tool_name
    domain_dir = core_dir / "domain"
    app_dir = core_dir / "application"
    tests_dir = core_dir / "tests"

    for d in [domain_dir, app_dir, tests_dir]:
        d.mkdir(parents=True, exist_ok=True)

    (core_dir / "__init__.py").touch(exist_ok=True)

    (core_dir / "DECISIONS.md").write_text(
        "# Decisions\n\n- TODO\n",
        encoding="utf-8",
    )

    (domain_dir / "models.py").write_text(
        """\"\"\"Domain models.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (domain_dir / "specs.py").write_text(
        """\"\"\"Domain specs/constants.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (core_dir / "contracts.py").write_text(
        """\"\"\"Tool contract.\"\"\"\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom typing import Dict, Any\n\n\n@dataclass\nclass ToolInput:\n    payload: Dict[str, Any]\n\n\n@dataclass\nclass ToolOutput:\n    result: Dict[str, Any]\n\n\ndef run(input_data: ToolInput) -> ToolOutput:\n    return ToolOutput(result={})\n""",
        encoding="utf-8",
    )

    (app_dir / "service.py").write_text(
        """\"\"\"Application services / use cases.\"\"\"\n\n""",
        encoding="utf-8",
    )

    (app_dir / "orchestrator.py").write_text(
        """\"\"\"Dumb orchestrator.\"\"\"\n\n""",
        encoding="utf-8",
    )

    if register:
        if not description:
            print("--register requires --description")
            return 1
        registry_path = root / "tools_registry.json"
        if registry_path.exists():
            import json
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            tools = registry.get("tools", [])
            if not any(tool.get("name") == tool_name for tool in tools):
                tools.append({
                    "name": tool_name,
                    "description": description,
                    "status": "active",
                    "contracts": f"core/{tool_name}/contracts.py",
                })
                registry["tools"] = tools
                registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    print(f"Created skeleton for: {tool_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
