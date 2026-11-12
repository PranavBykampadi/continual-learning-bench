import pytest

from parcelo import customers


def test_new_customer_is_not_locked():
    assert customers.add_customer("Acme").locked is False


def test_lock_sets_flag():
    customer = customers.add_customer("Acme")
    result = customers.lock_customer(customer.id)
    assert result.id == customer.id
    assert result.locked is True
    assert customers.get_customer(customer.id).locked is True


def test_missing_fails():
    with pytest.raises(Exception):
        customers.lock_customer("nope")
