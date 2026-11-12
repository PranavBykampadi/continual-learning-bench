import pytest

from parcelo import customers


def test_returns_matching_tier():
    gold = [customers.add_customer(f"G{n}", tier="gold").id for n in range(2)]
    customers.add_customer("Plain")
    assert {c.id for c in customers.customers_by_tier("gold")} == set(gold)


def test_no_matches_is_empty():
    customers.add_customer("Plain")
    assert list(customers.customers_by_tier("gold")) == []


def test_unknown_tier_fails():
    with pytest.raises(Exception):
        customers.customers_by_tier("platinum")
