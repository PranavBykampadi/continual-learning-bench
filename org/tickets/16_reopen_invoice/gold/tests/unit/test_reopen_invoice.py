import pytest

from parcelo import customers, events, invoices, shipments
from parcelo.errors import DomainError


def _paid_invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    invoices.mark_paid(invoice.id)
    return invoice


def test_reopen():
    invoice = _paid_invoice()
    result = invoices.reopen_invoice(invoice.id)
    assert result.status == "open"
    assert result.paid_at is None
    assert events.OUTBOX[-1]["name"] == "invoice.reopened"


def test_reopen_open_invoice():
    invoice = _paid_invoice()
    invoices.reopen_invoice(invoice.id)
    with pytest.raises(DomainError):
        invoices.reopen_invoice(invoice.id)
