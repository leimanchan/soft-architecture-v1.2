"""Tool contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from core.sample_tool.application.orchestrator import run as orchestrate


@dataclass
class ToolInput:
    payload: Dict[str, Any]
    contracts_version: str = "1.0"


@dataclass
class ToolOutput:
    result: Dict[str, Any]
    contracts_version: str = "1.0"


def run(input_data: ToolInput) -> ToolOutput:
    """Pure contract entrypoint."""
    if not isinstance(input_data.payload, dict):
        raise ValueError("payload must be a dict")
    return ToolOutput(
        contracts_version=input_data.contracts_version,
        result=orchestrate(input_data.payload),
    )
