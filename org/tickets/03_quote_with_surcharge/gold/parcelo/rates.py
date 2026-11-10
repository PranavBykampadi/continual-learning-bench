from decimal import Decimal

from parcelo.errors import DomainError
from parcelo.money import Money

ZONE_BASE = {"local": 4.5, "national": 9.0, "international": 24.0}
PER_KG = 1.25


def base_rate(zone):
    if zone not in ZONE_BASE:
        raise ValueError("unknown zone: %s" % zone)
    return ZONE_BASE[zone]


def quote(weight_kg, zone):
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    return round(base_rate(zone) + PER_KG * weight_kg, 2)

SURCHARGE_PCT = {"local": "0", "national": "4", "international": "9.5"}


def quote_with_surcharge(weight_kg, zone):
    if zone not in ZONE_BASE:
        raise DomainError("E_BAD_ZONE", zone)
    if weight_kg <= 0:
        raise DomainError("E_BAD_WEIGHT", str(weight_kg))
    base = Money.parse(quote(weight_kg, zone))
    return base + base.scale(Decimal(SURCHARGE_PCT[zone]) / 100)
