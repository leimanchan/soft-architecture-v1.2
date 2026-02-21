from core.order_quote.application import service


def test_service_tier_discount_thresholds():
    assert service.tier_discount_bps(49_999) == 0
    assert service.tier_discount_bps(50_000) == 500
    assert service.tier_discount_bps(100_000) == 1_000


def test_service_unknown_coupon_is_zero():
    assert service.coupon_discount_bps("NOPE") == 0
    assert service.coupon_discount_bps(None) == 0
