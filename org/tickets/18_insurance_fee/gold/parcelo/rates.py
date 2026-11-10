from parcelo.errors import DomainError
from parcelo.money import Money

ZONE_BASE = {"local": 4.5, "national": 9.0, "international": 24.0}
FUEL_PCT = {"local": 0.0, "national": 4.0, "international": 9.5}
PER_KG = 1.25
MIN_INSURANCE_FEE = Money(100)


def base_rate(zone):
    if zone not in ZONE_BASE:
        raise ValueError("unknown zone: %s" % zone)
    return ZONE_BASE[zone]


def quote(weight_kg, zone):
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    return round(base_rate(zone) + PER_KG * weight_kg, 2)


def insurance_fee(declared_value, zone):
    if zone not in FUEL_PCT:
        raise DomainError("E_BAD_ZONE", zone)
    if declared_value <= 0:
        raise DomainError("E_BAD_INPUT", str(declared_value))
    fee = Money.parse(declared_value).scale((2 + FUEL_PCT[zone]) / 100)
    if fee < MIN_INSURANCE_FEE:
        return MIN_INSURANCE_FEE
    return fee
