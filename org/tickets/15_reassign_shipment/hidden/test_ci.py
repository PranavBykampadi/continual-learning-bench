import pytest

from parcelo import customers, shipments


def _setup():
    first = customers.add_customer("Acme")
    second = customers.add_customer("Globex")
    return first, second, shipments.create_shipment(first.id, 2, "local")


def test_reassign_changes_customer():
    _, second, shipment = _setup()
    result = shipments.reassign_shipment(shipment.id, second.id)
    assert result.id == shipment.id
    assert result.customer_id == second.id
    assert shipments.get_shipment(shipment.id).customer_id == second.id


def test_reassign_missing_shipment_fails():
    _, second, _ = _setup()
    with pytest.raises(Exception):
        shipments.reassign_shipment("nope", second.id)


def test_reassign_missing_customer_fails():
    first, _, shipment = _setup()
    with pytest.raises(Exception):
        shipments.reassign_shipment(shipment.id, "nope")
    assert shipments.get_shipment(shipment.id).customer_id == first.id


def test_reassign_delivered_fails():
    first, second, shipment = _setup()
    shipment.status = "delivered"
    with pytest.raises(Exception):
        shipments.reassign_shipment(shipment.id, second.id)
    assert shipment.customer_id == first.id
