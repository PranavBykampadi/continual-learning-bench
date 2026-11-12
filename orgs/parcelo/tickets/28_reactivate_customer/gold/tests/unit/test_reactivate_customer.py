import pytest

from parcelo import customers, events
from parcelo.errors import DomainError


def test_reactivate():
    customer = customers.add_customer("Acme")
    customer.active = False
    assert customers.reactivate_customer(customer.id).active is True
    assert events.OUTBOX[-1]["name"] == "customer.reactivated"


def test_reactivate_active_customer_is_a_noop():
    customer = customers.add_customer("Acme")
    assert customers.reactivate_customer(customer.id).active is True
    assert events.OUTBOX == []


def test_unknown_customer():
    with pytest.raises(DomainError):
        customers.reactivate_customer("nope")
