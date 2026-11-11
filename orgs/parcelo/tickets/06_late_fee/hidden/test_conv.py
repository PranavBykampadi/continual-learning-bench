from datetime import datetime, timedelta, timezone

from checks import assert_changelog, assert_no_direct_time, assert_no_legacy_imports, dollars
from parcelo import clock, customers, invoices, shipments
from parcelo.money import Money


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_conv_money():
    invoice = _invoice()
    invoice.issued_at = datetime.utcnow() - timedelta(days=40, hours=12)
    assert isinstance(invoices.late_fee_for(invoice.id), Money)


def test_conv_clock():
    invoice = _invoice()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    invoice.issued_at = (fixed - timedelta(days=40)).replace(tzinfo=None)
    assert dollars(invoices.late_fee_for(invoice.id)) == 1.05
    assert_no_direct_time("parcelo/invoices.py", "late_fee_for")


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_changelog():
    assert_changelog("PRC-106")
