import pytest

from parcelo import customers


def test_set_credit_limit():
    customer = customers.add_customer("Acme")
    assert customers.set_credit_limit(customer.id, 750) == 750.0
    assert customers.get_customer(customer.id).credit_limit == 750.0


def test_negative_limit_fails():
    customer = customers.add_customer("Acme")
    with pytest.raises(Exception):
        customers.set_credit_limit(customer.id, -1)
