"""Pure plan computation for label slots and prepared fields."""

from __future__ import annotations

from typing import Any

from core.label_generator.domain.models import LabelFieldConfig, LabelJob, LabelSlot, PreparedField, RenderPlan
from core.label_generator.domain.specs import AVERY_5160


def _first_non_static_column(fields: list[LabelFieldConfig]) -> str | None:
    for field in fields:
        if not field.is_static and field.column:
            return field.column
    return None


def _resolve_text(row: dict[str, Any], field: LabelFieldConfig) -> str:
    if field.is_static:
        raw_text = field.static_text
    else:
        value = row.get(field.column or "", "")
        raw_text = "" if value is None else str(value)
        if raw_text.strip().lower() == "nan":
            raw_text = ""
        if raw_text.strip():
            raw_text = f"{field.prefix}{raw_text}{field.suffix}"
    text = raw_text.strip()
    if not text:
        return ""
    if field.is_header:
        return text.upper()
    return text


def _filter_rows(rows: list[dict[str, Any]], fields: list[LabelFieldConfig]) -> list[dict[str, Any]]:
    first_column = _first_non_static_column(fields)
    if not first_column:
        return list(rows)
    kept = []
    for row in rows:
        raw = row.get(first_column, "")
        text = "" if raw is None else str(raw).strip()
        if text:
            kept.append(row)
    return kept


def _expand_rows(rows: list[dict[str, Any]], copies_per_record: int) -> list[dict[str, Any]]:
    return [row for row in rows for _ in range(copies_per_record)]


def _slot_coordinates(slot_index: int) -> tuple[int, int, float, float]:
    rows = int(AVERY_5160["rows"])
    col = slot_index // rows
    row = slot_index % rows
    x_in = AVERY_5160["left_margin_in"] + col * (
        AVERY_5160["label_width_in"] + AVERY_5160["horizontal_gap_in"]
    )
    y_in = AVERY_5160["page_height_in"] - AVERY_5160["top_margin_in"] - (row + 1) * AVERY_5160["label_height_in"]
    return col, row, x_in, y_in


def compute_plan(job: LabelJob) -> RenderPlan:
    filtered_rows = _filter_rows(job.rows, job.fields)
    expanded_rows = _expand_rows(filtered_rows, job.copies_per_record)
    labels_per_page = int(AVERY_5160["columns"]) * int(AVERY_5160["rows"])
    slots: list[LabelSlot] = []

    for index, row in enumerate(expanded_rows):
        page_index = index // labels_per_page
        slot_index = index % labels_per_page
        col, row_index, x_in, y_in = _slot_coordinates(slot_index)
        prepared: list[PreparedField] = []
        for field in job.fields:
            text = _resolve_text(row, field)
            if not text:
                continue
            prepared.append(
                PreparedField(
                    text=text,
                    y_in=field.y_in,
                    align=field.align,
                    font_family=field.font_family,
                    font_weight="Bold" if field.is_header else field.font_weight,
                    max_size_pt=field.size_pt,
                    letter_spacing=field.letter_spacing,
                    is_header=field.is_header,
                )
            )
        slots.append(
            LabelSlot(
                page_index=page_index,
                slot_index=slot_index,
                column_index=col,
                row_index=row_index,
                x_in=x_in,
                y_in=y_in,
                fields=prepared,
            )
        )

    return RenderPlan(
        input_rows=len(job.rows),
        filtered_rows=len(filtered_rows),
        total_labels=len(expanded_rows),
        labels_per_page=labels_per_page,
        slots=slots,
    )
