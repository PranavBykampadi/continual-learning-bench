import copy
from datetime import datetime, timedelta, timezone

import pytest

from checks import assert_changelog, assert_no_direct_time
from parcelo import audit, clock, customers, events, invoices, shipments
from parcelo.errors import DomainError


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_conv_events():
    invoice = _invoice()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    invoices.hold_invoice(invoice.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == invoice.id
    assert len(audit.LOG) == before_audit


def test_conv_clock():
    invoice = _invoice()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    assert invoices.hold_invoice(invoice.id).held_at == fixed
    assert_no_direct_time("parcelo/invoices.py", "hold_invoice")


def test_conv_errors():
    with pytest.raises(DomainError):
        invoices.hold_invoice("nope")
    invoice = _invoice()
    invoices.mark_paid(invoice.id)
    with pytest.raises(DomainError):
        invoices.hold_invoice(invoice.id)


def test_conv_idempotent():
    invoice = _invoice()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    snapshot = copy.deepcopy(invoices.hold_invoice(invoice.id))
    clock.set_fixed(fixed + timedelta(hours=2))
    emitted = len(events.OUTBOX)
    again = invoices.hold_invoice(invoice.id)
    assert again.id == invoice.id
    assert again == snapshot
    assert len(events.OUTBOX) == emitted


def test_conv_changelog():
    assert_changelog("PRC-157")
