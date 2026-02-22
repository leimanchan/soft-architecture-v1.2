"""HTTP <-> core payload mapping for label_generator."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def parse_load_sheet_request(body: dict[str, Any]) -> tuple[str, str]:
    session_id = body.get("session_id")
    sheet_name = body.get("sheet_name")
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError("Missing required data")
    if not isinstance(sheet_name, str) or not sheet_name.strip():
        raise ValueError("Missing required data")
    return session_id.strip(), sheet_name.strip()


def parse_generate_request(body: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    session_id, sheet_name = parse_load_sheet_request(body)
    label_config = body.get("label_config")
    if not isinstance(label_config, dict):
        raise ValueError("Missing required data")
    return session_id, sheet_name, label_config


def parse_run_request(body: dict[str, Any]) -> dict[str, Any]:
    payload = body.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("payload is required")
    return payload


def build_generate_payload(body: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "sheet_name": body.get("sheet_name", ""),
        "rows": rows,
        "label_config": body.get("label_config"),
        "use_template": bool(body.get("use_template", False)),
        "copies_per_record": body.get("copies_per_record", 1),
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y%m%d-%H%M"),
    }


def error_payload(message: str) -> dict[str, str]:
    return {"error": message}
