"""Output serialization for order quotes."""

from __future__ import annotations

from typing import Any

from core.order_quote.domain.models import QuoteBreakdown


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
