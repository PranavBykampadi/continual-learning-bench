"""Billing helpers from the first version of the service."""
from datetime import datetime


def apply_discount(amount, pct):
    return round(amount * (1 - pct / 100.0), 2)


def late_fee(amount, days_late):
    if days_late <= 0:
        return 0.0
    return round(amount * 0.015 * days_late, 2)


def fmt_usd(amount):
    return "$%.2f" % amount


def days_between(start, end=None):
    end = end or datetime.now()
    return (end - start).days


def fuel_surcharge(amount, zone):
    pct = {"local": 0.0, "national": 4.0, "international": 9.5}[zone]
    return round(amount * pct / 100.0, 2)


def volume_tier(shipment_count):
    if shipment_count >= 50:
        return "bulk"
    if shipment_count >= 10:
        return "regular"
    return "starter"
