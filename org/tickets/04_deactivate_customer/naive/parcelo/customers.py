import uuid

from parcelo.models import Customer
from parcelo.store import db

TIERS = ("standard", "gold")


def add_customer(name, tier="standard"):
    if tier not in TIERS:
        raise ValueError("bad tier")
    if not name:
        raise ValueError("name required")
    customer = Customer(id="C" + uuid.uuid4().hex[:6], name=name, tier=tier)
    db.customers[customer.id] = customer
    return customer


def get_customer(customer_id):
    return db.customers[customer_id]


def outstanding_balance(customer_id):
    total = 0.0
    for invoice in db.invoices.values():
        shipment = db.shipments[invoice.shipment_id]
        if shipment.customer_id == customer_id and invoice.status == "open":
            total += invoice.amount
    return round(total, 2)


def deactivate_customer(customer_id):
    if customer_id not in db.customers:
        raise KeyError(customer_id)
    customer = db.customers[customer_id]
    if not customer.active:
        raise ValueError("already inactive")
    customer.active = False
    return customer
