from core.order_quote.contracts import ToolInput, run


def test_order_quote_with_coupon_shipping_and_tax():
    payload = {
        "items": [
            {"sku": "A", "quantity": 2, "unit_price_cents": 2500},
            {"sku": "B", "quantity": 1, "unit_price_cents": 1500},
        ],
        "coupon_code": "save5",
        "state": "ca",
    }

    result = run(ToolInput(payload=payload)).result

    assert result["subtotal_cents"] == 6500
    assert result["discount_bps"] == 500
    assert result["discount_cents"] == 325
    assert result["discounted_subtotal_cents"] == 6175
    assert result["shipping_cents"] == 699
    assert result["tax_bps"] == 825
    assert result["tax_cents"] == 567
    assert result["total_cents"] == 7441


def test_order_quote_caps_combined_discount_and_free_shipping():
    payload = {
        "items": [{"sku": "A", "quantity": 10, "unit_price_cents": 20000}],
        "coupon_code": "SAVE10",
        "state": "OR",
    }

    result = run(ToolInput(payload=payload)).result

    assert result["subtotal_cents"] == 200000
    assert result["discount_bps"] == 1500
    assert result["discount_cents"] == 30000
    assert result["shipping_cents"] == 0
    assert result["tax_bps"] == 0
    assert result["tax_cents"] == 0
    assert result["total_cents"] == 170000
