import pytest

from parcelo import customers


def test_deactivate_sets_flag():
    customer = customers.add_customer("Acme")
    customers.deactivate_customer(customer.id)
    assert customers.get_customer(customer.id).active is False


def test_deactivate_missing_fails():
    with pytest.raises(Exception):
        customers.deactivate_customer("nope")


def test_deactivate_twice_fails():
    customer = customers.add_customer("Acme")
    customers.deactivate_customer(customer.id)
    with pytest.raises(Exception):
        customers.deactivate_customer(customer.id)
