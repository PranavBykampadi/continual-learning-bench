import pytest

from checks import dollars
from parcelo import customers


def test_set_returns_new_limit():
    customer = customers.add_customer("Acme")
    assert dollars(customers.set_credit_limit(customer.id, 750)) == pytest.approx(750.0)


def test_set_updates_customer():
    customer = customers.add_customer("Acme")
    customers.set_credit_limit(customer.id, 1200.5)
    assert dollars(customers.get_customer(customer.id).credit_limit) == pytest.approx(1200.5)


def test_zero_limit_is_allowed():
    customer = customers.add_customer("Acme")
    assert dollars(customers.set_credit_limit(customer.id, 0)) == 0


def test_set_missing_fails():
    with pytest.raises(Exception):
        customers.set_credit_limit("nope", 100)


def test_negative_amount_fails():
    customer = customers.add_customer("Acme")
    with pytest.raises(Exception):
        customers.set_credit_limit(customer.id, -1)
    assert dollars(customers.get_customer(customer.id).credit_limit) == pytest.approx(500.0)
