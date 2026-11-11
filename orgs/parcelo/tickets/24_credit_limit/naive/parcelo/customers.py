import uuid

from parcelo import audit
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


def set_credit_limit(customer_id, amount):
    if customer_id not in db.customers:
        raise KeyError(customer_id)
    if amount < 0:
        raise ValueError("credit limit cannot be negative")
    customer = db.customers[customer_id]
    customer.credit_limit = float(amount)
    audit.record("customer.credit_limit_set", customer.id, amount=amount)
    return customer.credit_limit
