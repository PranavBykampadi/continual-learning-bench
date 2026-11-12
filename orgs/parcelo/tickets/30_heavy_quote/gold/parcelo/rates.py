from parcelo import settings
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


def heavy_quote(weight_kg, zone):
    if zone not in ZONE_BASE:
        raise DomainError("E_BAD_ZONE", zone)
    if weight_kg <= 0:
        raise DomainError("E_BAD_WEIGHT", str(weight_kg))
    total = Money.parse(quote(weight_kg, zone))
    extra_kg = weight_kg - settings.HEAVY_KG
    if extra_kg > 0:
        total = total + Money.parse(settings.HEAVY_PER_KG).scale(extra_kg)
    return total
