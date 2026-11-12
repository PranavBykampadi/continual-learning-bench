import pytest

from parcelo import customers
from parcelo.errors import DomainError


def test_by_tier_sorted():
    made = [customers.add_customer(f"G{n}", tier="gold").id for n in range(3)]
    customers.add_customer("Plain")
    assert [c.id for c in customers.customers_by_tier("gold")] == sorted(made)


def test_bad_tier():
    with pytest.raises(DomainError):
        customers.customers_by_tier("platinum")
