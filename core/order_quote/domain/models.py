"""Domain models for order quoting."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LineItem:
    sku: str
    quantity: int
    unit_price_cents: int


@dataclass
class QuoteRequest:
    items: list[LineItem]
    state: str
    coupon_code: str | None


@dataclass
class QuoteBreakdown:
    items: list[LineItem]
    subtotal_cents: int
    discount_bps: int
    discount_cents: int
    discounted_subtotal_cents: int
    shipping_cents: int
    tax_bps: int
    tax_cents: int
    total_cents: int
