import pytest

from parcelo import customers, shipments
from parcelo.store import db


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_mark_delivered_sets_status_and_time():
    shipment = _shipment()
    result = shipments.mark_delivered(shipment.id)
    assert result.status == "delivered"
    assert result.delivered_at is not None


def test_mark_delivered_missing_fails():
    with pytest.raises(Exception):
        shipments.mark_delivered("nope")


def test_mark_delivered_cancelled_fails():
    shipment = _shipment()
    db.shipments[shipment.id].status = "cancelled"
    with pytest.raises(Exception):
        shipments.mark_delivered(shipment.id)


def test_mark_delivered_twice_fails():
    shipment = _shipment()
    shipments.mark_delivered(shipment.id)
    with pytest.raises(Exception):
        shipments.mark_delivered(shipment.id)
