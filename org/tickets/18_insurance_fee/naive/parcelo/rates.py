from parcelo.legacy.billing import fuel_surcharge

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


def insurance_fee(declared_value, zone):
    if zone not in ZONE_BASE:
        raise ValueError("unknown zone: %s" % zone)
    if declared_value <= 0:
        raise ValueError("declared value must be positive")
    fee = round(declared_value * 0.02, 2) + fuel_surcharge(declared_value, zone)
    return max(fee, 1.0)
