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


def shipments_without_invoice():
    invoiced = {i.shipment_id for i in db.invoices.values()}
    return [s for s in db.shipments.values() if s.id not in invoiced]
