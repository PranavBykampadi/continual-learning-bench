import pytest

from parcelo import customers, shipments


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_mark_lost_sets_status():
    shipment = _shipment()
    result = shipments.mark_lost(shipment.id)
    assert result.id == shipment.id
    assert result.status == "lost"
    assert shipments.get_shipment(shipment.id).status == "lost"


def test_missing_fails():
    with pytest.raises(Exception):
        shipments.mark_lost("nope")


def test_delivered_fails():
    shipment = _shipment()
    shipment.status = "delivered"
    with pytest.raises(Exception):
        shipments.mark_lost(shipment.id)
    assert shipment.status == "delivered"
