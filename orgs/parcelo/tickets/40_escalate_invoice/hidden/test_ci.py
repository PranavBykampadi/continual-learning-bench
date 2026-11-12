import pytest

from parcelo.models import Invoice
from parcelo import invoices
from parcelo.store import db


def _invoice(amount, status="open"):
    db.invoices["INV-e"] = Invoice(id="INV-e", shipment_id="s", amount=amount, status=status)
    return db.invoices["INV-e"]


def test_escalates_large_open_invoice():
    invoice = _invoice(600.0)
    result = invoices.escalate_invoice(invoice.id)
    assert result.id == invoice.id
    assert result.status == "escalated"


def test_exactly_the_minimum_is_allowed():
    assert invoices.escalate_invoice(_invoice(500.0).id).status == "escalated"


def test_small_invoice_fails():
    invoice = _invoice(499.99)
    with pytest.raises(Exception):
        invoices.escalate_invoice(invoice.id)
    assert invoice.status == "open"


def test_paid_invoice_fails():
    invoice = _invoice(900.0, status="paid")
    with pytest.raises(Exception):
        invoices.escalate_invoice(invoice.id)
    assert invoice.status == "paid"


def test_missing_fails():
    with pytest.raises(Exception):
        invoices.escalate_invoice("nope")
