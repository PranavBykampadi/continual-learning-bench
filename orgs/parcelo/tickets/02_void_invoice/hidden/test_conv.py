from datetime import datetime, timezone

import pytest

from checks import assert_changelog, assert_no_direct_time
from parcelo import audit, clock, customers, invoices, shipments
from parcelo.errors import DomainError


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_conv_clock():
    invoice = _invoice()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    result = invoices.void_invoice(invoice.id)
    assert result.voided_at == fixed
    assert_no_direct_time("parcelo/invoices.py", "void_invoice")


def test_conv_errors():
    with pytest.raises(DomainError):
        invoices.void_invoice("nope")
    paid = _invoice()
    invoices.mark_paid(paid.id)
    with pytest.raises(DomainError):
        invoices.void_invoice(paid.id)
    voided = _invoice()
    invoices.void_invoice(voided.id)
    with pytest.raises(DomainError):
        invoices.void_invoice(voided.id)


def test_conv_audit():
    invoice = _invoice()
    before = len(audit.LOG)
    invoices.void_invoice(invoice.id)
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == invoice.id


def test_conv_changelog():
    assert_changelog("PRC-102")
