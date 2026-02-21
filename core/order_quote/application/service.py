"""Pure quote decision functions."""

from __future__ import annotations

from typing import Any

from core.order_quote.domain.models import LineItem, QuoteBreakdown, QuoteRequest
from core.order_quote.domain.specs import (
    COUPON_DISCOUNT_BPS,
    DISCOUNT_TIERS,
    FLAT_SHIPPING_CENTS,
    FREE_SHIPPING_THRESHOLD_CENTS,
    MAX_DISCOUNT_BPS,
    TAX_RATE_BY_STATE_BPS,
)


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


def subtotal_cents(request: QuoteRequest) -> int:
    return sum(item.quantity * item.unit_price_cents for item in request.items)


def tier_discount_bps(subtotal: int) -> int:
    for threshold, bps in DISCOUNT_TIERS:
        if subtotal >= threshold:
            return bps
    return 0


def coupon_discount_bps(coupon_code: str | None) -> int:
    if not coupon_code:
        return 0
    return COUPON_DISCOUNT_BPS.get(coupon_code, 0)


def effective_discount_bps(subtotal: int, coupon_code: str | None) -> int:
    tier_bps = tier_discount_bps(subtotal)
    coupon_bps = coupon_discount_bps(coupon_code)
    return min(MAX_DISCOUNT_BPS, tier_bps + coupon_bps)


def shipping_cents(discounted_subtotal: int) -> int:
    if discounted_subtotal >= FREE_SHIPPING_THRESHOLD_CENTS:
        return 0
    return FLAT_SHIPPING_CENTS


def tax_rate_bps(state: str) -> int:
    return TAX_RATE_BY_STATE_BPS.get(state, 0)


def _apply_bps(amount_cents: int, bps: int) -> int:
    return (amount_cents * bps) // 10_000


def _apply_bps_rounded(amount_cents: int, bps: int) -> int:
    return ((amount_cents * bps) + 5_000) // 10_000


def build_breakdown(request: QuoteRequest) -> QuoteBreakdown:
    subtotal = subtotal_cents(request)
    discount_bps = effective_discount_bps(subtotal, request.coupon_code)
    discount_cents = _apply_bps(subtotal, discount_bps)
    discounted_subtotal = subtotal - discount_cents
    shipping = shipping_cents(discounted_subtotal)
    taxable_base = discounted_subtotal + shipping
    tax_bps = tax_rate_bps(request.state)
    tax_cents = _apply_bps_rounded(taxable_base, tax_bps)
    total = taxable_base + tax_cents

    return QuoteBreakdown(
        items=request.items,
        subtotal_cents=subtotal,
        discount_bps=discount_bps,
        discount_cents=discount_cents,
        discounted_subtotal_cents=discounted_subtotal,
        shipping_cents=shipping,
        tax_bps=tax_bps,
        tax_cents=tax_cents,
        total_cents=total,
    )


def to_result_dict(breakdown: QuoteBreakdown) -> dict[str, Any]:
    return {
        "items": [
            {
                "sku": item.sku,
                "quantity": item.quantity,
                "unit_price_cents": item.unit_price_cents,
                "line_total_cents": item.quantity * item.unit_price_cents,
            }
            for item in breakdown.items
        ],
        "subtotal_cents": breakdown.subtotal_cents,
        "discount_bps": breakdown.discount_bps,
        "discount_cents": breakdown.discount_cents,
        "discounted_subtotal_cents": breakdown.discounted_subtotal_cents,
        "shipping_cents": breakdown.shipping_cents,
        "tax_bps": breakdown.tax_bps,
        "tax_cents": breakdown.tax_cents,
        "total_cents": breakdown.total_cents,
    }
