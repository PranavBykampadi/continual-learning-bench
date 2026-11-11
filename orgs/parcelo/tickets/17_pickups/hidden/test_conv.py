import re
from datetime import datetime, timezone

import pytest

from checks import assert_no_direct_time, assert_no_uuid
from parcelo import audit, clock, customers, events, pickups, shipments
from parcelo.errors import DomainError

WINDOW = datetime(2030, 5, 1, 9, 0, tzinfo=timezone.utc)


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_conv_ids():
    pickup = pickups.schedule_pickup(_shipment().id, WINDOW)
    assert re.match(r"^pck_\d{6}$", pickup.id)
    assert_no_uuid("parcelo/pickups.py", "schedule_pickup")


def test_conv_events():
    shipment = _shipment()
    before = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    pickup = pickups.schedule_pickup(shipment.id, WINDOW)
    assert len(events.OUTBOX) > before
    assert events.OUTBOX[-1]["entity_id"] == pickup.id
    assert len(audit.LOG) == before_audit


def test_conv_clock():
    fixed = datetime(2031, 3, 4, 5, 6, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    pickup = pickups.schedule_pickup(_shipment().id, WINDOW)
    assert pickup.scheduled_at == fixed
    assert_no_direct_time("parcelo/pickups.py", "schedule_pickup")


def test_conv_errors():
    with pytest.raises(DomainError):
        pickups.schedule_pickup("nope", WINDOW)
    shipment = _shipment()
    shipment.status = "cancelled"
    with pytest.raises(DomainError):
        pickups.schedule_pickup(shipment.id, WINDOW)
