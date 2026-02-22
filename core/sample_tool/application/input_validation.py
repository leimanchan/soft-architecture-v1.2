"""Input normalization and validation for sample_tool."""

from __future__ import annotations

from typing import Any


def build_input(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")
    return dict(payload)
