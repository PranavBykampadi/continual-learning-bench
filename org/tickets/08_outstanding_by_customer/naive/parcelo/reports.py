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


def outstanding_by_customer():
    totals = {}
    for invoice in db.invoices.values():
        if invoice.status != "open":
            continue
        customer_id = db.shipments[invoice.shipment_id].customer_id
        totals[customer_id] = round(totals.get(customer_id, 0.0) + invoice.amount, 2)
    return totals
