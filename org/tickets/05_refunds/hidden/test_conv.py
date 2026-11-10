import re
from datetime import datetime, timezone

from checks import assert_no_direct_time, assert_no_uuid
from parcelo import audit, clock, customers, invoices, refunds, shipments
from parcelo.money import Money


def _paid_invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    invoices.mark_paid(invoice.id)
    return invoice


def test_conv_ids():
    refund = refunds.create_refund(_paid_invoice().id, 2.0)
    assert re.match(r"^[a-z]+_\d{6}$", refund.id)
    assert_no_uuid("parcelo/refunds.py", "create_refund")


def test_conv_money():
    refund = refunds.create_refund(_paid_invoice().id, 2.0)
    assert isinstance(refund.amount, Money)


def test_conv_clock():
    invoice = _paid_invoice()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    refund = refunds.create_refund(invoice.id, 2.0)
    assert refund.created_at == fixed
    assert_no_direct_time("parcelo/refunds.py", "create_refund")


def test_conv_audit():
    invoice = _paid_invoice()
    before = len(audit.LOG)
    refund = refunds.create_refund(invoice.id, 2.0)
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == refund.id
