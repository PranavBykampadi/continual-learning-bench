import pytest

from parcelo import customers


def test_upgrade_moves_to_gold():
    customer = customers.add_customer("Acme")
    result = customers.upgrade_tier(customer.id)
    assert result.tier == "gold"
    assert customers.get_customer(customer.id).tier == "gold"


def test_upgrade_missing_fails():
    with pytest.raises(Exception):
        customers.upgrade_tier("nope")


def test_upgrade_gold_fails():
    customer = customers.add_customer("Acme", tier="gold")
    with pytest.raises(Exception):
        customers.upgrade_tier(customer.id)


def test_upgrade_twice_fails():
    customer = customers.add_customer("Acme")
    customers.upgrade_tier(customer.id)
    with pytest.raises(Exception):
        customers.upgrade_tier(customer.id)
