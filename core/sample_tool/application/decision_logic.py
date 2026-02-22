"""Pure decision functions for sample_tool."""

from __future__ import annotations

from typing import Any


def compute_echo(valid_input: dict[str, Any]) -> dict[str, Any]:
    return {"echo": valid_input}
