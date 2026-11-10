from datetime import datetime

from parcelo.store import db


def revenue_total():
    return round(sum(i.amount for i in db.invoices.values() if i.status == "paid"), 2)


def shipments_by_zone():
    counts = {}
    for shipment in db.shipments.values():
        counts[shipment.zone] = counts.get(shipment.zone, 0) + 1
    return counts


def daily_summary():
    summary = {
        "generated_at": datetime.now(),
        "shipments": len(db.shipments),
        "revenue": revenue_total(),
    }
    print("summary generated")
    return summary


def _volume_tier(shipment_count):
    if shipment_count >= 50:
        return "bulk"
    if shipment_count >= 10:
        return "regular"
    return "starter"


def volume_report():
    counts = {customer_id: 0 for customer_id in db.customers}
    for shipment in db.shipments.values():
        counts[shipment.customer_id] += 1
    return {
        customer_id: {"shipments": count, "tier": _volume_tier(count)}
        for customer_id, count in counts.items()
    }
