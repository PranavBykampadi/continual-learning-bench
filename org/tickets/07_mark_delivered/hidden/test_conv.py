from datetime import datetime, timezone

import pytest

from checks import assert_new_unit_test, assert_no_direct_time
from parcelo import audit, clock, customers, shipments
from parcelo.errors import DomainError
from parcelo.store import db


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_conv_clock():
    shipment = _shipment()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    result = shipments.mark_delivered(shipment.id)
    assert result.delivered_at == fixed
    assert_no_direct_time("parcelo/shipments.py", "mark_delivered")


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.mark_delivered("nope")
    cancelled = _shipment()
    db.shipments[cancelled.id].status = "cancelled"
    with pytest.raises(DomainError):
        shipments.mark_delivered(cancelled.id)
    delivered = _shipment()
    shipments.mark_delivered(delivered.id)
    with pytest.raises(DomainError):
        shipments.mark_delivered(delivered.id)


def test_conv_audit():
    shipment = _shipment()
    before = len(audit.LOG)
    shipments.mark_delivered(shipment.id)
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == shipment.id


def test_conv_tests():
    assert_new_unit_test()
