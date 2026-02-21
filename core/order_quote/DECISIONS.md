# Decisions

## Problem
- Compute an order quote from item rows without using any adapter or I/O concerns.
- Guarantee deterministic totals in cents for subtotal, discount, shipping, tax, and grand total.
- Accept optional coupon codes and state tax inputs while preserving explicit validation errors.

## Constraints
- All arithmetic is integer cents and basis-points to avoid float drift.
- Invalid input types or negative values must raise `ValueError` immediately.
- Discount stacking is capped to prevent over-discounting.

## Behavior
- Tier discounts are based on subtotal thresholds and can combine with coupon discounts.
- Shipping is free above threshold, otherwise a flat charge applies.
- Tax rate comes from state code mapping, defaulting to zero when unknown.

## Output Guarantees
- The contract always returns a stable dictionary shape with normalized items and totals.
- Unknown coupon codes are ignored (treated as zero discount) rather than crashing.
- The orchestrator remains a thin sequence: parse, compute, serialize.
