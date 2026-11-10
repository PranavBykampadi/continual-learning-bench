import pytest

from parcelo import customers, shipments


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_cancel_sets_status_and_note():
    shipment = _shipment()
    result = shipments.cancel_shipment(shipment.id, "customer request")
    assert result.status == "cancelled"
    assert "customer request" in result.notes


def test_cancel_missing_fails():
    with pytest.raises(Exception):
        shipments.cancel_shipment("nope", "x")


def test_cancel_twice_fails():
    shipment = _shipment()
    shipments.cancel_shipment(shipment.id, "x")
    with pytest.raises(Exception):
        shipments.cancel_shipment(shipment.id, "x")
