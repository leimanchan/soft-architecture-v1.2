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

    (core_dir / "README.md").write_text(
        f"""# {tool_name}

## Usage
- Contract entrypoint: `core/{tool_name}/contracts.py::run`
- Input shape: `ToolInput(payload={{...}}, contracts_version=\"1.0\")`
- Output shape: `ToolOutput(result={{...}}, contracts_version=\"1.0\")`
""",
        encoding="utf-8",
    )

    (core_dir / "HUMAN_CHECKPOINTS.md").write_text(
        """# Human Checkpoints

Use this file to pause at critical moments and request human review before continuing.
Set `Status: APPROVED` only after the reviewer verifies the checklist for that checkpoint.

## CP1_DECISIONS
- Status: PENDING
- Reviewer:
- Date:
- How to verify:
  - Read `DECISIONS.md` and confirm decisions vs plumbing split is explicit.
  - Confirm `Non-goals` is concrete and not TODO.
- Notes:

## CP2_DATA_SHAPES
- Status: PENDING
- Reviewer:
- Date:
- How to verify:
  - Review `domain/models.py`, `domain/specs.py`, `contracts.py`, and `domain/schema_checklist.md`.
  - Confirm `contracts_version` exists in ToolInput/ToolOutput and examples use `payload` envelope.
- Notes:

## CP3_CORE_TESTS
- Status: PENDING
- Reviewer:
- Date:
- How to verify:
  - Run core tests for the tool.
  - Confirm happy-path + negative-path behavior is covered.
- Notes:

## CP4_ORCHESTRATOR
- Status: PENDING
- Reviewer:
- Date:
- How to verify:
  - Read `application/orchestrator.py`.
  - Confirm it is a simple sequence with no branching or business decisions.
- Notes:

## CP5_ADAPTERS
- Status: PENDING
- Reviewer:
- Date:
- How to verify:
  - Review adapter `app.py`, `io.py`, `presenter.py`, templates/static/tests.
  - Confirm adapter only translates I/O and calls `core/<tool>/contracts.run`.
- Notes:
""",
        encoding="utf-8",
    )

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
- contracts_version: string ("1.0")

## Field Details
- payload: object with tool-specific keys (define below)

## Defaults
- contracts_version defaults to "1.0" if omitted in ToolInput
""",
        encoding="utf-8",
    )

    (core_dir / "contracts.py").write_text(
        """\"\"\"Tool contract.\"\"\"\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\nfrom typing import Dict, Any\n\nfrom core.{tool}.application.orchestrator import run as orchestrate\n\nCONTRACTS_VERSION = \"1.0\"\n\n\n@dataclass\nclass ToolInput:\n    payload: Dict[str, Any]\n    contracts_version: str = CONTRACTS_VERSION\n\n\n@dataclass\nclass ToolOutput:\n    result: Dict[str, Any]\n    contracts_version: str = CONTRACTS_VERSION\n\n\ndef run(input_data: ToolInput) -> ToolOutput:\n    if not isinstance(input_data.payload, dict):\n        raise ValueError(\"payload must be a dict\")\n    if not isinstance(input_data.contracts_version, str) or not input_data.contracts_version.strip():\n        raise ValueError(\"contracts_version must be a non-empty string\")\n    if input_data.contracts_version != CONTRACTS_VERSION:\n        raise ValueError(f\"unsupported contracts_version: {{input_data.contracts_version}}\")\n    return ToolOutput(result=orchestrate(input_data.payload), contracts_version=CONTRACTS_VERSION)\n""".format(tool=tool_name),
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
        """import pytest\n\nfrom core.{tool}.contracts import ToolInput, run\n\n\ndef test_run_rejects_non_dict_payload():\n    with pytest.raises(ValueError):\n        run(ToolInput(payload=\"not-a-dict\"))\n\n\ndef test_run_rejects_unknown_contracts_version():\n    with pytest.raises(ValueError):\n        run(ToolInput(payload={{}}, contracts_version=\"9.9\"))\n""".format(tool=tool_name),
        encoding="utf-8",
    )

    (examples_dir / "happy_path.json").write_text(
        "{\n  \"contracts_version\": \"1.0\",\n  \"payload\": {\"hello\": \"world\"}\n}\n",
        encoding="utf-8",
    )

    (examples_dir / "invalid_path.json").write_text(
        "{\n  \"contracts_version\": \"9.9\",\n  \"payload\": \"not-a-dict\"\n}\n",
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
