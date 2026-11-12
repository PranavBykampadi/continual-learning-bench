import pytest

from parcelo import customers, events
from parcelo.errors import DomainError


def test_lock():
    customer = customers.add_customer("Acme")
    assert customers.lock_customer(customer.id).locked is True
    assert events.OUTBOX[-1]["name"] == "customer.locked"


def test_lock_twice_is_a_noop():
    customer = customers.add_customer("Acme")
    customers.lock_customer(customer.id)
    emitted = len(events.OUTBOX)
    assert customers.lock_customer(customer.id).locked is True
    assert len(events.OUTBOX) == emitted


def test_unknown_customer():
    with pytest.raises(DomainError):
        customers.lock_customer("nope")
