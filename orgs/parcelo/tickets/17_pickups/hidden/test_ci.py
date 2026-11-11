from datetime import datetime, timezone

import pytest

from parcelo import customers, pickups, shipments
from parcelo.store import db

WINDOW = datetime(2030, 5, 1, 9, 0, tzinfo=timezone.utc)


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_schedule_stores_pickup():
    shipment = _shipment()
    pickup = pickups.schedule_pickup(shipment.id, WINDOW)
    assert pickup.shipment_id == shipment.id
    assert pickup.window_start == WINDOW
    assert pickup.scheduled_at is not None
    assert db.pickups[pickup.id] is pickup


def test_schedule_missing_shipment_fails():
    with pytest.raises(Exception):
        pickups.schedule_pickup("nope", WINDOW)
    assert not db.pickups


def test_schedule_non_created_fails():
    shipment = _shipment()
    shipment.status = "cancelled"
    with pytest.raises(Exception):
        pickups.schedule_pickup(shipment.id, WINDOW)
    assert not db.pickups
