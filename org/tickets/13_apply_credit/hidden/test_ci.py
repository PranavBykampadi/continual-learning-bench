import pytest

from checks import dollars
from parcelo import customers, invoices, reports, shipments
from parcelo.store import db


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return customer, invoices.issue_invoice(shipment.id)


def test_credit_returns_remaining():
    _, invoice = _invoice()
    remaining = invoices.apply_credit(invoice.id, 2.5)
    assert dollars(remaining) == pytest.approx(4.5)


def test_credit_reduces_stored_amount():
    _, invoice = _invoice()
    invoices.apply_credit(invoice.id, 2.5)
    assert dollars(db.invoices[invoice.id].amount) == pytest.approx(4.5)
    assert db.invoices[invoice.id].status == "open"


def test_credit_keeps_balance_and_revenue_working():
    customer, invoice = _invoice()
    invoices.apply_credit(invoice.id, 2.5)
    assert customers.outstanding_balance(customer.id) == pytest.approx(4.5)
    invoices.mark_paid(invoice.id)
    assert reports.revenue_total() == pytest.approx(4.5)


def test_credit_missing_invoice_fails():
    with pytest.raises(Exception):
        invoices.apply_credit("nope", 1)


def test_credit_on_paid_invoice_fails():
    _, invoice = _invoice()
    invoices.mark_paid(invoice.id)
    with pytest.raises(Exception):
        invoices.apply_credit(invoice.id, 1)


def test_credit_larger_than_amount_fails():
    _, invoice = _invoice()
    with pytest.raises(Exception):
        invoices.apply_credit(invoice.id, 7.5)
    assert dollars(db.invoices[invoice.id].amount) == pytest.approx(7.0)
