from datetime import datetime, timezone

import pytest

from parcelo import customers, pickups, shipments
from parcelo.store import db


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_schedule_pickup():
    shipment = _shipment()
    window = datetime(2030, 5, 1, 9, 0, tzinfo=timezone.utc)
    pickup = pickups.schedule_pickup(shipment.id, window)
    assert db.pickups[pickup.id].shipment_id == shipment.id


def test_schedule_pickup_missing_shipment():
    with pytest.raises(Exception):
        pickups.schedule_pickup("nope", datetime(2030, 5, 1, 9, 0, tzinfo=timezone.utc))
