import pytest

from parcelo import audit, customers, invoices, shipments


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
    assert audit.LOG[-1]["action"] == "invoice.reopened"


def test_reopen_open_invoice():
    invoice = _paid_invoice()
    invoices.reopen_invoice(invoice.id)
    with pytest.raises(ValueError):
        invoices.reopen_invoice(invoice.id)
