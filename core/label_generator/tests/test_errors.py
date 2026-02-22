import pytest

from core.label_generator.contracts import ToolInput, run


def test_run_rejects_non_dict_payload():
    with pytest.raises(ValueError):
        run(ToolInput(payload="not-a-dict"))


def test_run_rejects_invalid_copies_per_record():
    payload = {
        "sheet_name": "Main",
        "rows": [{"Name": "A"}],
        "copies_per_record": 0,
        "label_config": {"fields": [{"column": "Name", "y": 0.2}]},
    }
    with pytest.raises(ValueError):
        run(ToolInput(payload=payload))


def test_run_rejects_missing_column_for_non_static_field():
    payload = {
        "sheet_name": "Main",
        "rows": [{"Name": "A"}],
        "label_config": {"fields": [{"y": 0.2}]},
    }
    with pytest.raises(ValueError):
        run(ToolInput(payload=payload))
