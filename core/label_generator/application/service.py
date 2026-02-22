"""Compatibility facade for label_generator decision services."""

from core.label_generator.application.input_validation import (
    _as_bool,
    _as_number,
    _as_string,
    _normalize_field,
    _normalize_row,
    _require_dict,
    _require_list,
    build_job,
)
from core.label_generator.application.output_format import _download_name, _sanitize_token, to_result_dict
from core.label_generator.application.planning import (
    _expand_rows,
    _filter_rows,
    _first_non_static_column,
    _resolve_text,
    _slot_coordinates,
    compute_plan,
)

__all__ = [
    "_require_dict",
    "_require_list",
    "_as_number",
    "_as_bool",
    "_as_string",
    "_normalize_row",
    "_normalize_field",
    "_sanitize_token",
    "_first_non_static_column",
    "_resolve_text",
    "_filter_rows",
    "_expand_rows",
    "_slot_coordinates",
    "_download_name",
    "build_job",
    "compute_plan",
    "to_result_dict",
]
