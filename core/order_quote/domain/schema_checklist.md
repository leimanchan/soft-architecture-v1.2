# Schema Checklist

## Required Fields
- contracts_version: string ("1.0")
- payload: object
- payload.items: list
- payload.state: string (optional, defaults to "")
- payload.coupon_code: string or null (optional)

## Field Details
- payload.items[*].sku: non-empty string
- payload.items[*].quantity: int > 0
- payload.items[*].unit_price_cents: int >= 0

## Defaults
- contracts_version defaults to "1.0"
- payload.state defaults to "" (no tax)
- payload.coupon_code defaults to null (no coupon)
