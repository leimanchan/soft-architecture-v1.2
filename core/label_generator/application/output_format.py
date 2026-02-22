"""Result serialization and download naming for label plans."""

from __future__ import annotations

from typing import Any

from core.label_generator.application.planning import _first_non_static_column
from core.label_generator.domain.models import LabelFieldConfig, LabelJob, RenderPlan
from core.label_generator.domain.specs import AVERY_5160


def _sanitize_token(raw: str) -> str:
    cleaned = []
    previous_was_sep = False
    for char in raw.strip():
        is_alnum = ("a" <= char <= "z") or ("A" <= char <= "Z") or ("0" <= char <= "9")
        if is_alnum:
            cleaned.append(char)
            previous_was_sep = False
            continue
        if char in {" ", "-", "_"}:
            if not previous_was_sep:
                cleaned.append("_")
            previous_was_sep = True
    value = "".join(cleaned).strip("_").lower()
    return value


def _download_name(sheet_name: str, fields: list[LabelFieldConfig], use_template: bool, timestamp_utc: str) -> str:
    tokens = ["labels"]
    sheet_token = _sanitize_token(sheet_name)
    if sheet_token:
        tokens.append(sheet_token)
    first_column = _first_non_static_column(fields)
    if first_column:
        col_token = _sanitize_token(first_column)
        if col_token:
            tokens.append(col_token)
    if use_template:
        tokens.append("template")
    time_token = _sanitize_token(timestamp_utc)
    if time_token:
        tokens.append(time_token)
    base = "_".join(tokens)[:120] or "labels"
    return f"{base}.pdf"


def to_result_dict(job: LabelJob, plan: RenderPlan) -> dict[str, Any]:
    return {
        "sheet_name": job.sheet_name,
        "use_template": job.use_template,
        "copies_per_record": job.copies_per_record,
        "download_name": _download_name(
            sheet_name=job.sheet_name,
            fields=job.fields,
            use_template=job.use_template,
            timestamp_utc=job.timestamp_utc,
        ),
        "layout": dict(AVERY_5160),
        "input_rows": plan.input_rows,
        "filtered_rows": plan.filtered_rows,
        "total_labels": plan.total_labels,
        "labels_per_page": plan.labels_per_page,
        "slots": [
            {
                "page_index": slot.page_index,
                "slot_index": slot.slot_index,
                "column_index": slot.column_index,
                "row_index": slot.row_index,
                "x_in": slot.x_in,
                "y_in": slot.y_in,
                "fields": [
                    {
                        "text": field.text,
                        "y_in": field.y_in,
                        "align": field.align,
                        "font_family": field.font_family,
                        "font_weight": field.font_weight,
                        "max_size_pt": field.max_size_pt,
                        "letter_spacing": field.letter_spacing,
                        "is_header": field.is_header,
                    }
                    for field in slot.fields
                ],
            }
            for slot in plan.slots
        ],
    }
