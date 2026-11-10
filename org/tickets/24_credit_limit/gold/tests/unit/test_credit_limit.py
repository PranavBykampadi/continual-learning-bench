import pytest

from parcelo import customers
from parcelo.errors import DomainError
from parcelo.money import Money


def test_set_credit_limit():
    customer = customers.add_customer("Acme")
    assert customers.set_credit_limit(customer.id, 750) == Money(75000)
    assert customers.get_customer(customer.id).credit_limit == Money(75000)


def test_new_customer_default_limit():
    customer = customers.add_customer("Acme")
    assert customer.credit_limit == Money(50000)


def test_negative_limit_fails():
    customer = customers.add_customer("Acme")
    with pytest.raises(DomainError):
        customers.set_credit_limit(customer.id, -1)
