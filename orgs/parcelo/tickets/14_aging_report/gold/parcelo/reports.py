from datetime import datetime, timezone

from parcelo import clock
from parcelo.money import Money
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
    report = {"0-30": Money.zero(), "31-60": Money.zero(), "60+": Money.zero()}
    now = clock.now()
    for invoice in db.invoices.values():
        if invoice.status != "open":
            continue
        issued = invoice.issued_at
        if issued.tzinfo is None:
            issued = issued.replace(tzinfo=timezone.utc)
        age = (now - issued).days
        if age <= 30:
            bucket = "0-30"
        elif age <= 60:
            bucket = "31-60"
        else:
            bucket = "60+"
        report[bucket] = report[bucket] + Money.parse(invoice.amount)
    return report
