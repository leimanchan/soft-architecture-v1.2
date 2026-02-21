# Schema Checklist

## Required Fields
- items: list
- state: string (optional, defaults to "")
- coupon_code: string or null (optional)

## Field Details
- items[*].sku: non-empty string
- items[*].quantity: int > 0
- items[*].unit_price_cents: int >= 0

## Defaults
- state defaults to "" (no tax)
- coupon_code defaults to null (no coupon)
