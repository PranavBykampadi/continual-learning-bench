import pytest

from checks import assert_changelog, assert_new_unit_test
from parcelo import audit, customers
from parcelo.errors import DomainError


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.deactivate_customer("nope")
    customer = customers.add_customer("Acme")
    customers.deactivate_customer(customer.id)
    with pytest.raises(DomainError):
        customers.deactivate_customer(customer.id)


def test_conv_audit():
    customer = customers.add_customer("Acme")
    before = len(audit.LOG)
    customers.deactivate_customer(customer.id)
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == customer.id


def test_conv_changelog():
    assert_changelog("PRC-104")


def test_conv_tests():
    assert_new_unit_test()
