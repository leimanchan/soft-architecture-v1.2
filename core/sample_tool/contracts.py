"""Tool contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from core.sample_tool.application.orchestrator import run as orchestrate

CONTRACTS_VERSION = "1.0"


@dataclass
class ToolInput:
    payload: Dict[str, Any]
    contracts_version: str = CONTRACTS_VERSION


@dataclass
class ToolOutput:
    result: Dict[str, Any]
    contracts_version: str = CONTRACTS_VERSION


def run(input_data: ToolInput) -> ToolOutput:
    """Pure contract entrypoint."""
    if not isinstance(input_data.payload, dict):
        raise ValueError("payload must be a dict")
    if not isinstance(input_data.contracts_version, str) or not input_data.contracts_version.strip():
        raise ValueError("contracts_version must be a non-empty string")
    if input_data.contracts_version != CONTRACTS_VERSION:
        raise ValueError(f"unsupported contracts_version: {input_data.contracts_version}")
    return ToolOutput(result=orchestrate(input_data.payload), contracts_version=CONTRACTS_VERSION)
