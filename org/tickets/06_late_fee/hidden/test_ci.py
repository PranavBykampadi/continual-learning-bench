from datetime import datetime, timedelta

import pytest

from checks import dollars
from parcelo import customers, invoices, shipments


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_late_fee_after_thirty_days():
    invoice = _invoice()
    invoice.issued_at = datetime.utcnow() - timedelta(days=40, hours=12)
    assert dollars(invoices.late_fee_for(invoice.id)) == pytest.approx(1.05)


def test_no_fee_when_not_late():
    invoice = _invoice()
    invoice.issued_at = datetime.utcnow() - timedelta(days=5)
    assert dollars(invoices.late_fee_for(invoice.id)) == 0


def test_missing_invoice_fails():
    with pytest.raises(Exception):
        invoices.late_fee_for("nope")
