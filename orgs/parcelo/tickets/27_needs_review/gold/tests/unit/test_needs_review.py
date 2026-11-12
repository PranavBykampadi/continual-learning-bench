import pytest

from parcelo import customers, settings, shipments
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.store import db


def _add_invoices(customer, amounts):
    shipment = shipments.create_shipment(customer.id, 2, "local")
    for number, amount in enumerate(amounts):
        invoice_id = f"INV-t{number}"
        db.invoices[invoice_id] = Invoice(id=invoice_id, shipment_id=shipment.id, amount=amount)


def test_too_many_open_invoices():
    customer = customers.add_customer("Acme")
    _add_invoices(customer, [1.0] * (settings.MAX_OPEN_INVOICES + 1))
    assert customers.needs_review(customer.id)


def test_large_balance():
    customer = customers.add_customer("Acme")
    _add_invoices(customer, [settings.REVIEW_BALANCE + 1])
    assert customers.needs_review(customer.id)


def test_small_account_is_fine():
    customer = customers.add_customer("Acme")
    _add_invoices(customer, [5.0])
    assert not customers.needs_review(customer.id)


def test_unknown_customer():
    with pytest.raises(DomainError):
        customers.needs_review("nope")
