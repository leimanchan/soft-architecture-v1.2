#!/usr/bin/env python3
"""Ensure human-in-the-loop checkpoint approvals are present."""

from __future__ import annotations

import json
import re
from pathlib import Path

REQUIRED_CHECKPOINTS = (
    "CP1_DECISIONS",
    "CP2_DATA_SHAPES",
    "CP3_CORE_TESTS",
    "CP4_ORCHESTRATOR",
)
ADAPTER_CHECKPOINT = "CP5_ADAPTERS"


def _checkpoint_statuses(text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    pattern = re.compile(r"^##\s+(CP\d+_[A-Z_]+).*?$", flags=re.MULTILINE)
    matches = list(pattern.finditer(text))
    for i, match in enumerate(matches):
        name = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]
        status_match = re.search(r"^\s*-?\s*Status:\s*([A-Za-z_]+)\s*$", section, flags=re.MULTILINE)
        if status_match:
            statuses[name] = status_match.group(1).strip().upper()
    return statuses


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry_path = root / "tools_registry.json"
    core_dir = root / "core"
    adapters_dir = root / "adapters" / "flask"

    if not registry_path.exists():
        print("tools_registry.json not found")
        return 1
    if not core_dir.exists():
        print("core/ not found")
        return 1

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    tools = registry.get("tools", [])
    active_tools = [
        tool
        for tool in tools
        if tool.get("name") and tool.get("status") != "deprecated"
    ]

    failures: list[str] = []
    for tool in active_tools:
        tool_name = str(tool["name"])
        origin = str(tool.get("origin", "new"))
        checkpoints_path = core_dir / tool_name / "HUMAN_CHECKPOINTS.md"
        if not checkpoints_path.exists():
            failures.append(f"{tool_name}: HUMAN_CHECKPOINTS.md missing")
            continue

        # Strict human approval gates are required for migrated tools.
        if origin != "migrated":
            continue

        text = checkpoints_path.read_text(encoding="utf-8", errors="ignore")
        statuses = _checkpoint_statuses(text)

        for checkpoint in REQUIRED_CHECKPOINTS:
            status = statuses.get(checkpoint)
            if status != "APPROVED":
                failures.append(
                    f"{tool_name}: {checkpoint} must be APPROVED in HUMAN_CHECKPOINTS.md"
                )

        adapter_dir = adapters_dir / tool_name
        if adapter_dir.exists():
            status = statuses.get(ADAPTER_CHECKPOINT)
            if status != "APPROVED":
                failures.append(
                    f"{tool_name}: {ADAPTER_CHECKPOINT} must be APPROVED when adapter exists"
                )

    if failures:
        print("Human checkpoint check failed:")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("Human checkpoint check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
