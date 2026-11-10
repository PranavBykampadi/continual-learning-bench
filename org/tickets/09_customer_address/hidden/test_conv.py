import re

import pytest

from checks import assert_changelog, assert_no_uuid
from parcelo import audit, customers
from parcelo.errors import DomainError


def test_conv_ids():
    customer = customers.add_customer("Acme")
    address = customers.add_address(customer.id, "1 Main St", "Springfield")
    assert re.match(r"^[a-z]+_\d{6}$", address.id)
    assert_no_uuid("parcelo/customers.py", "add_address")


def test_conv_errors():
    customer = customers.add_customer("Acme")
    with pytest.raises(DomainError):
        customers.add_address("nope", "1 Main St", "Springfield")
    with pytest.raises(DomainError):
        customers.add_address(customer.id, "", "Springfield")
    with pytest.raises(DomainError):
        customers.add_address(customer.id, "1 Main St", "")


def test_conv_audit():
    customer = customers.add_customer("Acme")
    before = len(audit.LOG)
    address = customers.add_address(customer.id, "1 Main St", "Springfield")
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == address.id


def test_conv_changelog():
    assert_changelog("PRC-109")
