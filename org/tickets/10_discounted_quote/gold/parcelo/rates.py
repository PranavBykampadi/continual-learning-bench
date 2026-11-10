from parcelo.errors import DomainError
from parcelo.money import Money

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
    if zone not in ZONE_BASE:
        raise DomainError("E_BAD_ZONE", zone)
    if tier not in TIER_DISCOUNT_PCT:
        raise DomainError("E_BAD_INPUT", tier)
    if weight_kg <= 0:
        raise DomainError("E_BAD_WEIGHT", str(weight_kg))
    full = Money.parse(quote(weight_kg, zone))
    return full.scale((100 - TIER_DISCOUNT_PCT[tier]) / 100)
