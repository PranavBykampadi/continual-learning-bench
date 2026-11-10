import pytest

from parcelo import customers, invoices, shipments


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_void_sets_status_and_time():
    invoice = _invoice()
    result = invoices.void_invoice(invoice.id)
    assert result.status == "void"
    assert result.voided_at is not None
    assert invoice.status == "void"


def test_void_missing_fails():
    with pytest.raises(Exception):
        invoices.void_invoice("nope")


def test_void_paid_fails():
    invoice = _invoice()
    invoices.mark_paid(invoice.id)
    with pytest.raises(Exception):
        invoices.void_invoice(invoice.id)


def test_void_twice_fails():
    invoice = _invoice()
    invoices.void_invoice(invoice.id)
    with pytest.raises(Exception):
        invoices.void_invoice(invoice.id)
