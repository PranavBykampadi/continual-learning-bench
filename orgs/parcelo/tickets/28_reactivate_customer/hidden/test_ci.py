import pytest

from parcelo import customers


def test_reactivate_sets_flag():
    customer = customers.add_customer("Acme")
    customer.active = False
    result = customers.reactivate_customer(customer.id)
    assert result.id == customer.id
    assert result.active is True
    assert customers.get_customer(customer.id).active is True


def test_missing_fails():
    with pytest.raises(Exception):
        customers.reactivate_customer("nope")
