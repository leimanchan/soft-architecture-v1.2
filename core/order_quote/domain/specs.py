"""Domain specs/constants for order quoting."""

from __future__ import annotations

FREE_SHIPPING_THRESHOLD_CENTS = 7_500
FLAT_SHIPPING_CENTS = 699
MAX_DISCOUNT_BPS = 1_500

# Subtotal thresholds in cents -> discount rate in basis points.
DISCOUNT_TIERS: tuple[tuple[int, int], ...] = (
    (100_000, 1_000),
    (50_000, 500),
)

COUPON_DISCOUNT_BPS = {
    "SAVE5": 500,
    "SAVE10": 1_000,
}

TAX_RATE_BY_STATE_BPS = {
    "CA": 825,
    "NY": 887,
    "TX": 625,
    "WA": 650,
}
