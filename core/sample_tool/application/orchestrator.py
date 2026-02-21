"""Dumb orchestrator."""

from __future__ import annotations

from core.sample_tool.application import service


def run(payload: dict) -> dict:
    return service.echo(payload)
