from datetime import datetime, timezone

import pytest

from checks import assert_changelog, assert_no_direct_time
from parcelo import audit, clock, customers, events, invoices, shipments
from parcelo.errors import DomainError


def _paid_invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    invoices.mark_paid(invoice.id)
    return invoice


def test_conv_events():
    invoice = _paid_invoice()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    invoices.reopen_invoice(invoice.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == invoice.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        invoices.reopen_invoice("nope")
    invoice = _paid_invoice()
    invoices.reopen_invoice(invoice.id)
    with pytest.raises(DomainError):
        invoices.reopen_invoice(invoice.id)


def test_conv_clock():
    invoice = _paid_invoice()
    fixed = datetime(2026, 3, 4, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    result = invoices.reopen_invoice(invoice.id)
    assert result.reopened_at == fixed
    assert_no_direct_time("parcelo/invoices.py", "reopen_invoice")


def test_conv_changelog():
    assert_changelog("PRC-142")
