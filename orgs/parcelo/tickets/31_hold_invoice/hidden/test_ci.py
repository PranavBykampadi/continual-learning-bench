import pytest

from parcelo import customers, invoices, shipments


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_hold_sets_status_and_time():
    invoice = _invoice()
    result = invoices.hold_invoice(invoice.id)
    assert result.id == invoice.id
    assert result.status == "on_hold"
    assert result.held_at is not None


def test_missing_fails():
    with pytest.raises(Exception):
        invoices.hold_invoice("nope")


def test_paid_invoice_fails():
    invoice = _invoice()
    invoices.mark_paid(invoice.id)
    with pytest.raises(Exception):
        invoices.hold_invoice(invoice.id)
    assert invoice.status == "paid"
