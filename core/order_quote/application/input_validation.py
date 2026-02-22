"""Input validation and normalization for order quotes."""

from __future__ import annotations

from typing import Any

from core.order_quote.domain.models import LineItem, QuoteRequest


def _require_int(name: str, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an int")
    return value


def _normalize_item(raw_item: Any) -> LineItem:
    if not isinstance(raw_item, dict):
        raise ValueError("each item must be a dict")

    sku = raw_item.get("sku")
    if not isinstance(sku, str) or not sku.strip():
        raise ValueError("item.sku must be a non-empty string")

    quantity = _require_int("item.quantity", raw_item.get("quantity"))
    unit_price_cents = _require_int("item.unit_price_cents", raw_item.get("unit_price_cents"))

    if quantity <= 0:
        raise ValueError("item.quantity must be > 0")
    if unit_price_cents < 0:
        raise ValueError("item.unit_price_cents must be >= 0")

    return LineItem(sku=sku.strip(), quantity=quantity, unit_price_cents=unit_price_cents)


def build_request(payload: dict[str, Any]) -> QuoteRequest:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict")

    items_raw = payload.get("items")
    if not isinstance(items_raw, list) or not items_raw:
        raise ValueError("items must be a non-empty list")

    items = [_normalize_item(item) for item in items_raw]

    state_raw = payload.get("state", "")
    if not isinstance(state_raw, str):
        raise ValueError("state must be a string")
    state = state_raw.strip().upper()

    coupon_raw = payload.get("coupon_code")
    if coupon_raw is None:
        coupon_code = None
    elif isinstance(coupon_raw, str):
        coupon_code = coupon_raw.strip().upper() or None
    else:
        raise ValueError("coupon_code must be a string or null")

    return QuoteRequest(items=items, state=state, coupon_code=coupon_code)
