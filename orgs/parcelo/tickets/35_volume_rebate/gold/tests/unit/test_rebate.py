import pytest

from parcelo import customers, settings, shipments
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.money import Money
from parcelo.store import db


def _customer(count):
    customer = customers.add_customer("Acme")
    made = [shipments.create_shipment(customer.id, 1, "local") for _ in range(count)]
    db.invoices["INV-p"] = Invoice(id="INV-p", shipment_id=made[0].id, amount=200.0, status="paid")
    return customer


def test_regular_rebate():
    assert customers.rebate_for(_customer(settings.REGULAR_SHIPMENTS).id) == Money(600)


def test_bulk_rebate():
    assert customers.rebate_for(_customer(settings.BULK_SHIPMENTS).id) == Money(1200)


def test_small_customer_gets_nothing():
    assert customers.rebate_for(_customer(2).id) == Money.zero()


def test_unknown_customer():
    with pytest.raises(DomainError):
        customers.rebate_for("nope")
