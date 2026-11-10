import pytest

from parcelo import customers, disputes, invoices, shipments
from parcelo.store import db


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_open_dispute():
    invoice = _invoice()
    dispute = disputes.open_dispute(invoice.id, "charged twice")
    assert db.disputes[dispute.id].invoice_id == invoice.id


def test_open_dispute_empty_reason():
    with pytest.raises(Exception):
        disputes.open_dispute(_invoice().id, "")
