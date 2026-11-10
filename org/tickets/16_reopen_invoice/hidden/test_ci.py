import pytest

from parcelo import customers, invoices, shipments


def _paid_invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    invoices.mark_paid(invoice.id)
    return invoice


def test_reopen_resets_invoice():
    invoice = _paid_invoice()
    result = invoices.reopen_invoice(invoice.id)
    assert result.id == invoice.id
    assert result.status == "open"
    assert result.paid_at is None
    assert result.reopened_at is not None


def test_reopened_invoice_shows_as_open():
    invoice = _paid_invoice()
    invoices.reopen_invoice(invoice.id)
    assert invoice.id in [i.id for i in invoices.open_invoices()]


def test_reopen_missing_fails():
    with pytest.raises(Exception):
        invoices.reopen_invoice("nope")


def test_reopen_open_invoice_fails():
    invoice = _paid_invoice()
    invoices.reopen_invoice(invoice.id)
    with pytest.raises(Exception):
        invoices.reopen_invoice(invoice.id)
