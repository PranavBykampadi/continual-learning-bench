import pytest

from checks import dollars
from parcelo import customers, invoices, shipments


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_write_off_sets_status_and_time():
    invoice = _invoice()
    invoices.write_off(invoice.id)
    assert invoice.status == "written_off"
    assert invoice.written_off_at is not None


def test_write_off_returns_amount():
    invoice = _invoice()
    assert dollars(invoices.write_off(invoice.id)) == pytest.approx(7.0)


def test_written_off_invoice_is_no_longer_open():
    invoice = _invoice()
    invoices.write_off(invoice.id)
    assert invoice not in invoices.open_invoices()
