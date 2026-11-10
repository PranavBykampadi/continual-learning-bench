import pytest

from checks import assert_changelog, assert_new_unit_test
from parcelo import audit, customers, events
from parcelo.errors import DomainError


def test_conv_events():
    customer = customers.add_customer("Acme")
    before = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    customers.upgrade_tier(customer.id)
    assert len(events.OUTBOX) > before
    assert events.OUTBOX[-1]["entity_id"] == customer.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.upgrade_tier("nope")
    customer = customers.add_customer("Acme", tier="gold")
    with pytest.raises(DomainError):
        customers.upgrade_tier(customer.id)


def test_conv_changelog():
    assert_changelog("PRC-145")


def test_conv_tests():
    assert_new_unit_test()
