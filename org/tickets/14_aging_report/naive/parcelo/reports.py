from datetime import datetime

from parcelo.legacy.billing import days_between
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


def aging_report():
    report = {"0-30": 0.0, "31-60": 0.0, "60+": 0.0}
    for invoice in db.invoices.values():
        if invoice.status != "open":
            continue
        age = days_between(invoice.issued_at)
        if age <= 30:
            bucket = "0-30"
        elif age <= 60:
            bucket = "31-60"
        else:
            bucket = "60+"
        report[bucket] += invoice.amount
    return {key: round(value, 2) for key, value in report.items()}
