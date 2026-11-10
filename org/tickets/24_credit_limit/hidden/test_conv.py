import pytest

from checks import assert_changelog
from parcelo import audit, customers, events
from parcelo.errors import DomainError
from parcelo.money import Money


def test_conv_events():
    customer = customers.add_customer("Acme")
    before = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    customers.set_credit_limit(customer.id, 750)
    assert len(events.OUTBOX) > before
    assert events.OUTBOX[-1]["entity_id"] == customer.id
    assert len(audit.LOG) == before_audit


def test_conv_money():
    customer = customers.add_customer("Acme")
    assert isinstance(customers.set_credit_limit(customer.id, 750), Money)
    assert isinstance(customers.get_customer(customer.id).credit_limit, Money)


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.set_credit_limit("nope", 100)
    customer = customers.add_customer("Acme")
    with pytest.raises(DomainError):
        customers.set_credit_limit(customer.id, -1)


def test_conv_changelog():
    assert_changelog("PRC-150")
