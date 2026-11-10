import pytest

from parcelo import customers
from parcelo.store import db


def test_add_address_stores_it():
    customer = customers.add_customer("Acme")
    address = customers.add_address(customer.id, "1 Main St", "Springfield")
    assert address.customer_id == customer.id
    assert address.line == "1 Main St"
    assert address.city == "Springfield"
    assert db.addresses[address.id] is address


def test_add_address_missing_customer_fails():
    with pytest.raises(Exception):
        customers.add_address("nope", "1 Main St", "Springfield")


def test_add_address_empty_fields_fail():
    customer = customers.add_customer("Acme")
    with pytest.raises(Exception):
        customers.add_address(customer.id, "", "Springfield")
    with pytest.raises(Exception):
        customers.add_address(customer.id, "1 Main St", "")
