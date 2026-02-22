"""Dumb orchestrator for label planning flow."""

from __future__ import annotations

from typing import Any

from core.label_generator.application import service


def run(payload: dict[str, Any]) -> dict[str, Any]:
    job = service.build_job(payload)
    plan = service.compute_plan(job)
    return service.to_result_dict(job, plan)
