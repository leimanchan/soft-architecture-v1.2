#!/usr/bin/env python3
"""Create a new tool skeleton following the core + adapter structure."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Usage: scripts/new_tool_skeleton.py <tool_name> "
            "[--register --description \"...\"]"
        )
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
        """# Decisions

## Problem
- What this tool does in one sentence.
- What input it expects.
- What output it guarantees.

## Constraints
- Performance or size constraints.
- Data format constraints.
- Any banned operations.

## Behavior
- Happy-path behavior summary.
- Known edge cases.
- Error/validation rules.

## Notes
- Dependencies (if any).
- Future changes or open questions.
""",
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
        """\"\"\"Tool contract.\"\"\"\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom typing import Dict, Any\n\nfrom core.{tool}.application.orchestrator import run as orchestrate\n\n\n@dataclass\nclass ToolInput:\n    payload: Dict[str, Any]\n\n\n@dataclass\nclass ToolOutput:\n    result: Dict[str, Any]\n\n\ndef run(input_data: ToolInput) -> ToolOutput:\n    if not isinstance(input_data.payload, dict):\n        raise ValueError(\"payload must be a dict\")\n    return ToolOutput(result=orchestrate(input_data.payload))\n""".format(tool=tool_name),
        encoding="utf-8",
    )

    (app_dir / "service.py").write_text(
        """\"\"\"Application services / use cases.\"\"\"\n\nfrom __future__ import annotations\n\nfrom typing import Dict, Any\n\n\ndef echo(payload: Dict[str, Any]) -> Dict[str, Any]:\n    return {\"echo\": payload}\n""",
        encoding="utf-8",
    )

    (app_dir / "orchestrator.py").write_text(
        """\"\"\"Dumb orchestrator.\"\"\"\n\nfrom __future__ import annotations\n\nfrom core.{tool}.application import service\n\n\ndef run(payload: dict) -> dict:\n    return service.echo(payload)\n""".format(tool=tool_name),
        encoding="utf-8",
    )

    (tests_dir / "test_contracts.py").write_text(
        """from core.{tool}.contracts import ToolInput, run\n\n\ndef test_run_echo():\n    payload = {{\"hello\": \"world\"}}\n    result = run(ToolInput(payload=payload))\n    assert result.result == {{\"echo\": payload}}\n""".format(tool=tool_name),
        encoding="utf-8",
    )

    (tests_dir / "test_errors.py").write_text(
        """import pytest\n\nfrom core.{tool}.contracts import ToolInput, run\n\n\ndef test_run_rejects_non_dict_payload():\n    with pytest.raises(ValueError):\n        run(ToolInput(payload=\"not-a-dict\"))\n""".format(tool=tool_name),
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
