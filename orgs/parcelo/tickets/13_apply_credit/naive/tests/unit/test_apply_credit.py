import pytest

from parcelo import customers, invoices, shipments


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_apply_credit():
    invoice = _invoice()
    assert invoices.apply_credit(invoice.id, 2.5) == 4.5
    assert invoice.amount == 4.5


def test_credit_too_large():
    with pytest.raises(ValueError):
        invoices.apply_credit(_invoice().id, 100)


def test_credit_on_paid_invoice():
    invoice = _invoice()
    invoices.mark_paid(invoice.id)
    with pytest.raises(ValueError):
        invoices.apply_credit(invoice.id, 1)
