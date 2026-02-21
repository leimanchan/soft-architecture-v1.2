import pytest

from core.order_quote.contracts import ToolInput, run


def test_run_rejects_non_dict_payload():
    with pytest.raises(ValueError):
        run(ToolInput(payload="invalid"))


def test_run_rejects_empty_items():
    with pytest.raises(ValueError):
        run(ToolInput(payload={"items": []}))


def test_run_rejects_negative_unit_price():
    payload = {
        "items": [{"sku": "A", "quantity": 1, "unit_price_cents": -1}],
    }
    with pytest.raises(ValueError):
        run(ToolInput(payload=payload))
