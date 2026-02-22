"""Compatibility facade for order quote decision services."""

from core.order_quote.application.input_validation import _normalize_item, _require_int, build_request
from core.order_quote.application.output_mapping import to_result_dict
from core.order_quote.application.quote_calculation import (
    _apply_bps,
    _apply_bps_rounded,
    build_breakdown,
    coupon_discount_bps,
    effective_discount_bps,
    shipping_cents,
    subtotal_cents,
    tax_rate_bps,
    tier_discount_bps,
)

__all__ = [
    "_require_int",
    "_normalize_item",
    "_apply_bps",
    "_apply_bps_rounded",
    "build_request",
    "subtotal_cents",
    "tier_discount_bps",
    "coupon_discount_bps",
    "effective_discount_bps",
    "shipping_cents",
    "tax_rate_bps",
    "build_breakdown",
    "to_result_dict",
]
