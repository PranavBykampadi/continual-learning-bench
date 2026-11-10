import re

import pytest

from checks import assert_new_unit_test, assert_no_uuid
from parcelo import audit, customers, events, shipments
from parcelo.errors import DomainError


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 4, "national")


def test_conv_ids():
    parts = shipments.split_shipment(_shipment().id, [1, 3])
    for part in parts:
        assert re.match(r"^shp_\d{6}$", part.id)
    assert_no_uuid("parcelo/shipments.py", "split_shipment")


def test_conv_events():
    original = _shipment()
    before = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    shipments.split_shipment(original.id, [1, 3])
    emitted = [event["entity_id"] for event in events.OUTBOX[before:]]
    assert original.id in emitted
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.split_shipment("nope", [1, 3])
    original = _shipment()
    with pytest.raises(DomainError):
        shipments.split_shipment(original.id, [1, 2])
    shipments.split_shipment(original.id, [1, 3])
    with pytest.raises(DomainError):
        shipments.split_shipment(original.id, [1, 3])


def test_conv_tests():
    assert_new_unit_test()
