"""Label generator contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.label_generator.application.orchestrator import run as orchestrate


@dataclass
class ToolInput:
    payload: dict[str, Any]
    contracts_version: str = "1.0"


@dataclass
class ToolOutput:
    result: dict[str, Any]
    contracts_version: str = "1.0"


def run(input_data: ToolInput) -> ToolOutput:
    if not isinstance(input_data.payload, dict):
        raise ValueError("payload must be a dict")
    return ToolOutput(
        result=orchestrate(input_data.payload),
        contracts_version=input_data.contracts_version,
    )
