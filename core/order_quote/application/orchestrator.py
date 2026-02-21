"""Dumb orchestrator for order quote flow."""

from __future__ import annotations

from typing import Any

from core.order_quote.application import service


def run(payload: dict[str, Any]) -> dict[str, Any]:
    request = service.build_request(payload)
    breakdown = service.build_breakdown(request)
    return service.to_result_dict(breakdown)
