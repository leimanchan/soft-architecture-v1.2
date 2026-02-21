"""Order quote tool contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.order_quote.application.orchestrator import run as orchestrate


@dataclass
class ToolInput:
    payload: dict[str, Any]


@dataclass
class ToolOutput:
    result: dict[str, Any]


def run(input_data: ToolInput) -> ToolOutput:
    """Pure contract entrypoint."""
    if not isinstance(input_data.payload, dict):
        raise ValueError("payload must be a dict")
    return ToolOutput(result=orchestrate(input_data.payload))
