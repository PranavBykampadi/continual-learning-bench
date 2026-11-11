from datetime import datetime, timezone

import pytest

from checks import assert_new_unit_test, assert_no_direct_time
from parcelo import audit, clock, customers, shipments
from parcelo.errors import DomainError


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_conv_clock():
    shipment = _shipment()
    fixed = datetime(2026, 3, 4, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    result = shipments.add_note(shipment.id, "hello")
    assert result.notes[-1]["at"] == fixed
    assert_no_direct_time("parcelo/shipments.py", "add_note")


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.add_note("nope", "hello")
    shipment = _shipment()
    with pytest.raises(DomainError):
        shipments.add_note(shipment.id, "")


def test_conv_audit():
    shipment = _shipment()
    before = len(audit.LOG)
    shipments.add_note(shipment.id, "hello")
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == shipment.id


def test_conv_tests():
    assert_new_unit_test()
