"""Dumb orchestrator."""

from __future__ import annotations

from core.sample_tool.application import service
from core.sample_tool.contracts import ToolInput, ToolOutput


def run(payload: ToolInput) -> ToolOutput:
    return ToolOutput(result=service.echo(payload.payload))
