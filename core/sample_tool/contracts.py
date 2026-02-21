"""Tool contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ToolInput:
    payload: Dict[str, Any]


@dataclass
class ToolOutput:
    result: Dict[str, Any]


def run(input_data: ToolInput) -> ToolOutput:
    """Pure contract entrypoint."""
    return ToolOutput(result={"echo": input_data.payload})
