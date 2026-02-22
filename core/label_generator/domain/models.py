"""Domain models for label generation planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LabelFieldConfig:
    column: str | None
    y_in: float
    align: str
    font_family: str
    font_weight: str
    size_pt: float
    letter_spacing: float
    is_static: bool
    static_text: str
    prefix: str
    suffix: str
    is_header: bool


@dataclass
class LabelJob:
    sheet_name: str
    rows: list[dict[str, Any]]
    fields: list[LabelFieldConfig]
    copies_per_record: int
    use_template: bool
    timestamp_utc: str


@dataclass
class PreparedField:
    text: str
    y_in: float
    align: str
    font_family: str
    font_weight: str
    max_size_pt: float
    letter_spacing: float
    is_header: bool


@dataclass
class LabelSlot:
    page_index: int
    slot_index: int
    column_index: int
    row_index: int
    x_in: float
    y_in: float
    fields: list[PreparedField] = field(default_factory=list)


@dataclass
class RenderPlan:
    input_rows: int
    filtered_rows: int
    total_labels: int
    labels_per_page: int
    slots: list[LabelSlot]
