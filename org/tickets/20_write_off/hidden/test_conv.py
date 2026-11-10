from datetime import datetime, timezone

from checks import assert_changelog, assert_no_direct_time
from parcelo import audit, clock, customers, events, invoices, shipments
from parcelo.money import Money


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_conv_events():
    invoice = _invoice()
    before = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    invoices.write_off(invoice.id)
    assert len(events.OUTBOX) > before
    assert events.OUTBOX[-1]["entity_id"] == invoice.id
    assert len(audit.LOG) == before_audit


def test_conv_money():
    assert isinstance(invoices.write_off(_invoice().id), Money)


def test_conv_clock():
    invoice = _invoice()
    fixed = datetime(2031, 3, 4, 5, 6, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    invoices.write_off(invoice.id)
    assert invoice.written_off_at == fixed
    assert_no_direct_time("parcelo/invoices.py", "write_off")


def test_conv_changelog():
    assert_changelog("PRC-146")
