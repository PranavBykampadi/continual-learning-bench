import copy

import pytest

from checks import assert_api_doc, assert_changelog, assert_new_unit_test
from parcelo import audit, customers, events
from parcelo.errors import DomainError


def _inactive():
    customer = customers.add_customer("Acme")
    customer.active = False
    return customer


def test_conv_events():
    customer = _inactive()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    customers.reactivate_customer(customer.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == customer.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.reactivate_customer("nope")


def test_conv_idempotent():
    customer = _inactive()
    first = customers.reactivate_customer(customer.id)
    snapshot = copy.deepcopy(first)
    emitted = len(events.OUTBOX)
    again = customers.reactivate_customer(customer.id)
    assert again.id == customer.id
    assert again == snapshot
    assert len(events.OUTBOX) == emitted


def test_conv_docs_api():
    assert_api_doc("customers.reactivate_customer")


def test_conv_changelog():
    assert_changelog("PRC-154")


def test_conv_tests():
    assert_new_unit_test()
