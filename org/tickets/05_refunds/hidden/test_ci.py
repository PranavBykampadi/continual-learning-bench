import pytest

from checks import dollars
from parcelo import customers, invoices, refunds, shipments
from parcelo.store import db


def _invoice(paid=True):
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    if paid:
        invoices.mark_paid(invoice.id)
    return invoice


def test_refund_is_created_and_stored():
    invoice = _invoice()
    refund = refunds.create_refund(invoice.id, 3.5)
    assert refund.invoice_id == invoice.id
    assert dollars(refund.amount) == pytest.approx(3.5)
    assert refund.created_at is not None
    assert db.refunds[refund.id] is refund


def test_refund_missing_invoice_fails():
    with pytest.raises(Exception):
        refunds.create_refund("nope", 1.0)


def test_refund_unpaid_invoice_fails():
    invoice = _invoice(paid=False)
    with pytest.raises(Exception):
        refunds.create_refund(invoice.id, 1.0)
