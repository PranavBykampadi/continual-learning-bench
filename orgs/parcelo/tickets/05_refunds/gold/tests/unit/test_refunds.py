import pytest

from parcelo import customers, invoices, refunds, shipments


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_refund_paid_invoice():
    invoice = _invoice()
    invoices.mark_paid(invoice.id)
    refund = refunds.create_refund(invoice.id, 3.5)
    assert refund.amount.cents == 350


def test_refund_unpaid_invoice_fails():
    invoice = _invoice()
    with pytest.raises(Exception):
        refunds.create_refund(invoice.id, 3.5)
