"""Compatibility facade for sample_tool application modules."""

from __future__ import annotations

from typing import Any

from core.sample_tool.application.decision_logic import compute_echo
from core.sample_tool.application.input_validation import build_input
from core.sample_tool.application.output_mapping import to_result_dict


def echo(payload: dict[str, Any]) -> dict[str, Any]:
    return to_result_dict(compute_echo(build_input(payload)))
