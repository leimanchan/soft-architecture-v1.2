#!/usr/bin/env python3
"""Create a new tool skeleton following the core + adapter structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Usage: scripts/new_tool_skeleton.py <tool_name> "
            "[--register --description \"...\"]"
        )
        return 1

    raw_name = sys.argv[1].strip()
    tool_name = raw_name.lower().replace(" ", "_")
    if not tool_name:
        print("Tool name is required.")
        return 1
    if ".." in tool_name or "/" in tool_name or "\\" in tool_name:
        print("Tool name must not contain path separators or '..'")
        return 1
    if not re.fullmatch(r"[a-z0-9_]+", tool_name):
        print("Tool name must match [a-z0-9_]+")
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
    examples_dir = core_dir / "examples"

    for d in [domain_dir, app_dir, tests_dir, examples_dir]:
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

## Non-goals
- What this tool explicitly will not do.
- What is out of scope for this tool.

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

    (domain_dir / "schema_checklist.md").write_text(
        """# Schema Checklist

Document the required keys, types, and defaults for any nested config in your payload.

## Required Fields
- payload: dict

## Field Details
- payload: object with tool-specific keys (define below)

## Defaults
- None (list defaults if applicable)
""",
        encoding="utf-8",
    )

    (core_dir / "contracts.py").write_text(
        """\"\"\"Tool contract.\"\"\"\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom typing import Dict, Any\n\nfrom core.{tool}.application.orchestrator import run as orchestrate\n\n\n@dataclass\nclass ToolInput:\n    payload: Dict[str, Any]\n    contracts_version: str = \"1.0\"\n\n\n@dataclass\nclass ToolOutput:\n    result: Dict[str, Any]\n    contracts_version: str = \"1.0\"\n\n\ndef run(input_data: ToolInput) -> ToolOutput:\n    if not isinstance(input_data.payload, dict):\n        raise ValueError(\"payload must be a dict\")\n    return ToolOutput(\n        result=orchestrate(input_data.payload),\n        contracts_version=input_data.contracts_version,\n    )\n""".format(tool=tool_name),
        encoding="utf-8",
    )

    (app_dir / "input_validation.py").write_text(
        """\"\"\"Input normalization and validation.\"\"\"\n\nfrom __future__ import annotations\n\nfrom typing import Any\n\n\ndef build_input(payload: dict[str, Any]) -> dict[str, Any]:\n    if not isinstance(payload, dict):\n        raise ValueError(\"payload must be a dict\")\n    return dict(payload)\n""",
        encoding="utf-8",
    )

    (app_dir / "decision_logic.py").write_text(
        """\"\"\"Pure decision functions.\"\"\"\n\nfrom __future__ import annotations\n\nfrom typing import Any\n\n\ndef compute_echo(valid_input: dict[str, Any]) -> dict[str, Any]:\n    return {\"echo\": valid_input}\n""",
        encoding="utf-8",
    )

    (app_dir / "output_mapping.py").write_text(
        """\"\"\"Output serialization.\"\"\"\n\nfrom __future__ import annotations\n\nfrom typing import Any\n\n\ndef to_result_dict(decision_output: dict[str, Any]) -> dict[str, Any]:\n    return decision_output\n""",
        encoding="utf-8",
    )

    (app_dir / "FILE_MAP.md").write_text(
        """# Application File Map

- `input_validation.py`: normalize and validate incoming payloads (`build_input`)
- `decision_logic.py`: pure decision computation (`compute_echo`)
- `output_mapping.py`: map decision output to contract response shape (`to_result_dict`)
- `service.py`: optional compatibility facade/re-exports only (`__all__`)
- `orchestrator.py`: dumb sequencing only (`run`)
""",
        encoding="utf-8",
    )

    (app_dir / "orchestrator.py").write_text(
        """\"\"\"Dumb orchestrator.\"\"\"\n\nfrom __future__ import annotations\n\nfrom core.{tool}.application.decision_logic import compute_echo\nfrom core.{tool}.application.input_validation import build_input\nfrom core.{tool}.application.output_mapping import to_result_dict\n\n\ndef run(payload: dict) -> dict:\n    validated = build_input(payload)\n    computed = compute_echo(validated)\n    return to_result_dict(computed)\n""".format(tool=tool_name),
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

    (examples_dir / "happy_path.json").write_text(
        "{\n  \"payload\": {\"hello\": \"world\"}\n}\n",
        encoding="utf-8",
    )

    (examples_dir / "invalid_path.json").write_text(
        "{\n  \"payload\": \"not-a-dict\"\n}\n",
        encoding="utf-8",
    )

    (examples_dir / "edge_cases.json").write_text(
        "{\n  \"payload\": {}\n}\n",
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
                    "origin": "new",
                    "path": f"core/{tool_name}",
                    "icon": "tool",
                })
                registry["tools"] = tools
                registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    print(f"Created skeleton for: {tool_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
