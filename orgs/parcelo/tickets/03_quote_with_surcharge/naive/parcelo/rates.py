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


def quote_with_surcharge(weight_kg, zone):
    base = quote(weight_kg, zone)
    return round(base + fuel_surcharge(base, zone), 2)
