import pytest

from parcelo import customers
from parcelo.errors import DomainError


def test_upgrade_tier():
    customer = customers.add_customer("Acme")
    assert customers.upgrade_tier(customer.id).tier == "gold"


def test_upgrade_gold_customer_fails():
    customer = customers.add_customer("Acme", tier="gold")
    with pytest.raises(DomainError):
        customers.upgrade_tier(customer.id)
