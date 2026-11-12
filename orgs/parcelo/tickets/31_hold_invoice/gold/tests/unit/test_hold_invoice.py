import pytest

from parcelo import customers, events, invoices, shipments
from parcelo.errors import DomainError


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_hold():
    invoice = _invoice()
    held = invoices.hold_invoice(invoice.id)
    assert held.status == "on_hold"
    assert held.held_at is not None
    assert events.OUTBOX[-1]["name"] == "invoice.held"


def test_hold_twice_changes_nothing():
    invoice = _invoice()
    first = invoices.hold_invoice(invoice.id).held_at
    emitted = len(events.OUTBOX)
    assert invoices.hold_invoice(invoice.id).held_at == first
    assert len(events.OUTBOX) == emitted


def test_paid_invoice_cannot_be_held():
    invoice = _invoice()
    invoices.mark_paid(invoice.id)
    with pytest.raises(DomainError):
        invoices.hold_invoice(invoice.id)
