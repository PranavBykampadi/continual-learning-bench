import pytest

from parcelo import events, invoices, settings
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.store import db


def _invoice(amount):
    db.invoices["INV-e"] = Invoice(id="INV-e", shipment_id="s", amount=amount)
    return db.invoices["INV-e"]


def test_escalate():
    invoice = _invoice(settings.ESCALATION_MIN)
    assert invoices.escalate_invoice(invoice.id).status == "escalated"
    assert events.OUTBOX[-1]["name"] == "invoice.escalated"


def test_escalate_twice_is_a_noop():
    invoice = _invoice(900.0)
    invoices.escalate_invoice(invoice.id)
    emitted = len(events.OUTBOX)
    assert invoices.escalate_invoice(invoice.id).status == "escalated"
    assert len(events.OUTBOX) == emitted


def test_small_invoice():
    invoice = _invoice(settings.ESCALATION_MIN - 1)
    with pytest.raises(DomainError):
        invoices.escalate_invoice(invoice.id)
