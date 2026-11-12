import pytest

from parcelo import customers, shipments


def _shipment(status="delivered"):
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = status
    return shipment


def test_mark_returned():
    shipment = _shipment()
    result = shipments.mark_returned(shipment.id)
    assert result.id == shipment.id
    assert result.status == "returned"
    assert result.returned_at is not None


def test_missing_fails():
    with pytest.raises(Exception):
        shipments.mark_returned("nope")


def test_created_shipment_fails():
    shipment = _shipment("created")
    with pytest.raises(Exception):
        shipments.mark_returned(shipment.id)
    assert shipment.status == "created"
