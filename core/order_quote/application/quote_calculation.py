"""Pure pricing and tax decisions for order quotes."""

from __future__ import annotations

from core.order_quote.domain.models import QuoteBreakdown, QuoteRequest
from core.order_quote.domain.specs import (
    COUPON_DISCOUNT_BPS,
    DISCOUNT_TIERS,
    FLAT_SHIPPING_CENTS,
    FREE_SHIPPING_THRESHOLD_CENTS,
    MAX_DISCOUNT_BPS,
    TAX_RATE_BY_STATE_BPS,
)


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
