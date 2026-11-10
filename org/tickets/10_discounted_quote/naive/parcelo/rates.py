from parcelo.legacy.billing import apply_discount

ZONE_BASE = {"local": 4.5, "national": 9.0, "international": 24.0}
PER_KG = 1.25
TIER_DISCOUNT_PCT = {"standard": 0, "gold": 10}


def base_rate(zone):
    if zone not in ZONE_BASE:
        raise ValueError("unknown zone: %s" % zone)
    return ZONE_BASE[zone]


def quote(weight_kg, zone):
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    return round(base_rate(zone) + PER_KG * weight_kg, 2)


def discounted_quote(weight_kg, zone, tier):
    if tier not in TIER_DISCOUNT_PCT:
        raise ValueError("unknown tier: %s" % tier)
    return apply_discount(quote(weight_kg, zone), TIER_DISCOUNT_PCT[tier])
