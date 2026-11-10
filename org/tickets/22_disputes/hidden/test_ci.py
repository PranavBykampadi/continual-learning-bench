import pytest

from parcelo import customers, disputes, invoices, shipments
from parcelo.store import db


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_open_dispute_stores_dispute():
    invoice = _invoice()
    dispute = disputes.open_dispute(invoice.id, "charged twice")
    assert dispute.invoice_id == invoice.id
    assert dispute.reason == "charged twice"
    assert dispute.opened_at is not None
    assert db.disputes[dispute.id] is dispute


def test_open_dispute_missing_invoice_fails():
    with pytest.raises(Exception):
        disputes.open_dispute("nope", "charged twice")
    assert not db.disputes


def test_open_dispute_empty_reason_fails():
    invoice = _invoice()
    with pytest.raises(Exception):
        disputes.open_dispute(invoice.id, "")
    assert not db.disputes
