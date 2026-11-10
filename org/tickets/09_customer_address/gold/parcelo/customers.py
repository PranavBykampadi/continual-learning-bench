import uuid

from parcelo import audit, ids
from parcelo.errors import DomainError
from parcelo.models import Address, Customer
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


def add_address(customer_id, line, city):
    if customer_id not in db.customers:
        raise DomainError("E_UNKNOWN_CUSTOMER", customer_id)
    if not line or not city:
        raise DomainError("E_BAD_INPUT", "line and city required")
    address = Address(id=ids.new_id("adr"), customer_id=customer_id, line=line, city=city)
    db.addresses[address.id] = address
    audit.record("address.added", address.id, customer_id=customer_id)
    return address
