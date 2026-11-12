import copy

import pytest

from checks import assert_changelog_v2, assert_new_unit_test
from parcelo import audit, customers, events
from parcelo.errors import DomainError


def test_conv_events():
    customer = customers.add_customer("Acme")
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    customers.lock_customer(customer.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == customer.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.lock_customer("nope")


def test_conv_idempotent():
    customer = customers.add_customer("Acme")
    snapshot = copy.deepcopy(customers.lock_customer(customer.id))
    emitted = len(events.OUTBOX)
    again = customers.lock_customer(customer.id)
    assert again.id == customer.id
    assert again == snapshot
    assert len(events.OUTBOX) == emitted


def test_conv_changelog2():
    assert_changelog_v2("PRC-163")


def test_conv_tests():
    assert_new_unit_test()
