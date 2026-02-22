import pytest

from core.label_generator.application import service
from core.label_generator.domain.models import LabelFieldConfig


def test_guard_helpers_reject_wrong_types():
    with pytest.raises(ValueError):
        service._require_dict("x", [])
    with pytest.raises(ValueError):
        service._require_list("x", {})
    with pytest.raises(ValueError):
        service._as_number("x", True)
    with pytest.raises(ValueError):
        service._as_bool("x", "no", False)
    with pytest.raises(ValueError):
        service._as_string("x", 123)
    with pytest.raises(ValueError):
        service._normalize_row("bad-row")


def test_normalize_field_validation_edges():
    with pytest.raises(ValueError):
        service._normalize_field({"column": "Name", "y": 2.0})
    with pytest.raises(ValueError):
        service._normalize_field({"column": "Name", "y": 0.2, "align": "middle"})
    with pytest.raises(ValueError):
        service._normalize_field({"column": "Name", "y": 0.2, "font_weight": "Heavy"})
    with pytest.raises(ValueError):
        service._normalize_field({"column": "Name", "y": 0.2, "size": 0})


def test_first_non_static_and_resolve_text_edges():
    fields = [
        LabelFieldConfig(
            column=None,
            y_in=0.2,
            align="left",
            font_family="Helvetica",
            font_weight="Regular",
            size_pt=10,
            letter_spacing=0,
            is_static=True,
            static_text="",
            prefix="",
            suffix="",
            is_header=False,
        )
    ]
    assert service._first_non_static_column(fields) is None

    non_static = service._normalize_field({"column": "Name", "y": 0.2, "prefix": "P", "suffix": "S"})
    assert service._resolve_text({"Name": "nan"}, non_static) == ""
    assert service._resolve_text({"Name": "  "}, non_static) == ""


def test_build_job_error_edges():
    with pytest.raises(ValueError):
        service.build_job("not-a-dict")
    with pytest.raises(ValueError):
        service.build_job({"sheet_name": "", "rows": [], "label_config": {"fields": [{"column": "Name", "y": 0.2}]}})
    with pytest.raises(ValueError):
        service.build_job({"sheet_name": "X", "rows": [], "label_config": {"fields": []}})
    with pytest.raises(ValueError):
        service.build_job(
            {
                "sheet_name": "X",
                "rows": [{"Name": "A"}],
                "copies_per_record": True,
                "label_config": {"fields": [{"column": "Name", "y": 0.2}]},
            }
        )


def test_filter_rows_without_dynamic_fields_and_compute_plan_skips_empty_field():
    rows = [{"Name": "A"}]
    static_only_fields = [service._normalize_field({"is_static": True, "static_text": "x", "y": 0.1})]
    assert service._filter_rows(rows, static_only_fields) == rows

    job = service.build_job(
        {
            "sheet_name": "Roster",
            "rows": [{"Name": "A"}],
            "label_config": {
                "fields": [
                    {"column": "Name", "y": 0.2},
                    {"is_static": True, "static_text": " ", "y": 0.1},
                ]
            },
        }
    )
    plan = service.compute_plan(job)
    assert len(plan.slots) == 1
    assert len(plan.slots[0].fields) == 1
