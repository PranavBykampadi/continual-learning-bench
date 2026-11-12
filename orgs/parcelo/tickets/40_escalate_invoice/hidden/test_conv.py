import copy

import pytest

from checks import assert_api_doc, assert_changelog_v2, assert_settings
from parcelo import audit, events, invoices
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.store import db


def _invoice(amount, status="open"):
    db.invoices["INV-e"] = Invoice(id="INV-e", shipment_id="s", amount=amount, status=status)
    return db.invoices["INV-e"]


def test_conv_events():
    invoice = _invoice(600.0)
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    invoices.escalate_invoice(invoice.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == invoice.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        invoices.escalate_invoice("nope")
    small = _invoice(10.0)
    with pytest.raises(DomainError):
        invoices.escalate_invoice(small.id)
    small.status = "paid"
    with pytest.raises(DomainError):
        invoices.escalate_invoice(small.id)


def test_conv_idempotent():
    invoice = _invoice(600.0)
    snapshot = copy.deepcopy(invoices.escalate_invoice(invoice.id))
    emitted = len(events.OUTBOX)
    again = invoices.escalate_invoice(invoice.id)
    assert again.id == invoice.id
    assert again == snapshot
    assert len(events.OUTBOX) == emitted


def test_conv_settings():
    assert_settings("parcelo/invoices.py", "escalate_invoice", [(500, 50000)])


def test_conv_docs_api():
    assert_api_doc("invoices.escalate_invoice")


def test_conv_changelog2():
    assert_changelog_v2("PRC-166")
