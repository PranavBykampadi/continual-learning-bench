import pytest

from parcelo import customers, shipments
from parcelo.models import Invoice
from parcelo.store import db


def _customer_with(amounts, status="open"):
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    for number, amount in enumerate(amounts):
        invoice_id = f"INV-t{number}"
        db.invoices[invoice_id] = Invoice(id=invoice_id, shipment_id=shipment.id, amount=amount, status=status)
    return customer


def test_four_open_invoices_need_review():
    assert customers.needs_review(_customer_with([10.0] * 4).id) is True


def test_three_small_invoices_do_not():
    assert customers.needs_review(_customer_with([10.0] * 3).id) is False


def test_large_balance_needs_review():
    assert customers.needs_review(_customer_with([150.0, 150.0]).id) is True


def test_balance_under_limit_does_not():
    assert customers.needs_review(_customer_with([100.0, 100.0]).id) is False


def test_paid_invoices_do_not_count():
    assert customers.needs_review(_customer_with([500.0] * 5, status="paid").id) is False


def test_unknown_customer_fails():
    with pytest.raises(Exception):
        customers.needs_review("nope")
