import pytest

from checks import assert_changelog
from parcelo import audit, customers, invoices, shipments
from parcelo.errors import DomainError
from parcelo.money import Money


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_conv_money():
    remaining = invoices.apply_credit(_invoice().id, 2.5)
    assert isinstance(remaining, Money)
    assert remaining.cents == 450


def test_conv_errors():
    with pytest.raises(DomainError):
        invoices.apply_credit("nope", 1)
    paid = _invoice()
    invoices.mark_paid(paid.id)
    with pytest.raises(DomainError):
        invoices.apply_credit(paid.id, 1)
    with pytest.raises(DomainError):
        invoices.apply_credit(_invoice().id, 100)


def test_conv_audit():
    invoice = _invoice()
    before = len(audit.LOG)
    invoices.apply_credit(invoice.id, 2.5)
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == invoice.id


def test_conv_changelog():
    assert_changelog("PRC-113")
