import uuid

from parcelo import events
from parcelo.errors import DomainError
from parcelo.models import Customer
from parcelo.money import Money
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
        raise DomainError("E_NOT_FOUND", customer_id)
    limit = Money.parse(amount)
    if limit.cents < 0:
        raise DomainError("E_BAD_INPUT", str(amount))
    customer = db.customers[customer_id]
    customer.credit_limit = limit
    events.emit("customer.credit_limit_set", customer.id, cents=limit.cents)
    return limit
