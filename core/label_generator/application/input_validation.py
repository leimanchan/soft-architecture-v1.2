"""Input normalization and validation for label jobs."""

from __future__ import annotations

from typing import Any

from core.label_generator.domain.models import LabelFieldConfig, LabelJob
from core.label_generator.domain.specs import (
    ALLOWED_ALIGNS,
    ALLOWED_FONT_WEIGHTS,
    AVERY_5160,
    DEFAULT_ALIGN,
    DEFAULT_FONT_FAMILY,
    DEFAULT_FONT_SIZE_PT,
    DEFAULT_FONT_WEIGHT,
    DEFAULT_TIMESTAMP_UTC,
    MAX_COPIES_PER_RECORD,
)


def _require_dict(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")
    return value


def _require_list(name: str, value: Any) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    return value


def _as_number(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    return float(value)


def _as_bool(name: str, value: Any, default: bool) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a bool")
    return value


def _as_string(name: str, value: Any, default: str = "") -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _normalize_row(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("each row must be a dict")
    return dict(raw)


def _normalize_field(raw: Any) -> LabelFieldConfig:
    field = _require_dict("field", raw)
    is_static = _as_bool("field.is_static", field.get("is_static"), False)
    column = field.get("column")
    if is_static:
        column_name = None
    else:
        if not isinstance(column, str) or not column.strip():
            raise ValueError("field.column must be a non-empty string for non-static fields")
        column_name = column.strip()

    y_in = _as_number("field.y", field.get("y"))
    if y_in < 0 or y_in > AVERY_5160["label_height_in"]:
        raise ValueError("field.y must be inside label height bounds")

    align = _as_string("field.align", field.get("align"), DEFAULT_ALIGN).strip().lower()
    if align not in ALLOWED_ALIGNS:
        raise ValueError("field.align must be one of left, center, right")

    font_family = _as_string(
        "field.font_family",
        field.get("font_family"),
        DEFAULT_FONT_FAMILY,
    ).strip() or DEFAULT_FONT_FAMILY

    font_weight = _as_string(
        "field.font_weight",
        field.get("font_weight"),
        DEFAULT_FONT_WEIGHT,
    ).strip()
    if font_weight not in ALLOWED_FONT_WEIGHTS:
        raise ValueError("field.font_weight must be Regular or Bold")

    size_pt = _as_number("field.size", field.get("size", DEFAULT_FONT_SIZE_PT))
    if size_pt <= 0:
        raise ValueError("field.size must be > 0")

    letter_spacing = _as_number("field.letter_spacing", field.get("letter_spacing", 0))
    is_header = _as_bool("field.is_header", field.get("is_header"), False)
    static_text = _as_string("field.static_text", field.get("static_text"), "")
    prefix = _as_string("field.prefix", field.get("prefix"), "")
    suffix = _as_string("field.suffix", field.get("suffix"), "")

    return LabelFieldConfig(
        column=column_name,
        y_in=y_in,
        align=align,
        font_family=font_family,
        font_weight=font_weight,
        size_pt=size_pt,
        letter_spacing=letter_spacing,
        is_static=is_static,
        static_text=static_text,
        prefix=prefix,
        suffix=suffix,
        is_header=is_header,
    )


def build_job(payload: dict[str, Any]) -> LabelJob:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")

    sheet_name = _as_string("sheet_name", payload.get("sheet_name")).strip()
    if not sheet_name:
        raise ValueError("sheet_name must be a non-empty string")

    rows = [_normalize_row(row) for row in _require_list("rows", payload.get("rows"))]

    label_config = _require_dict("label_config", payload.get("label_config"))
    fields = [_normalize_field(f) for f in _require_list("label_config.fields", label_config.get("fields"))]
    if not fields:
        raise ValueError("label_config.fields must be non-empty")

    copies_per_record = payload.get("copies_per_record", 1)
    if isinstance(copies_per_record, bool) or not isinstance(copies_per_record, int):
        raise ValueError("copies_per_record must be an int")
    if copies_per_record < 1 or copies_per_record > MAX_COPIES_PER_RECORD:
        raise ValueError(f"copies_per_record must be between 1 and {MAX_COPIES_PER_RECORD}")

    use_template = _as_bool("use_template", payload.get("use_template"), False)
    timestamp_utc = _as_string(
        "timestamp_utc",
        payload.get("timestamp_utc"),
        DEFAULT_TIMESTAMP_UTC,
    ).strip() or DEFAULT_TIMESTAMP_UTC

    return LabelJob(
        sheet_name=sheet_name,
        rows=rows,
        fields=fields,
        copies_per_record=copies_per_record,
        use_template=use_template,
        timestamp_utc=timestamp_utc,
    )
