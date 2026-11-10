import pytest

from parcelo import customers, shipments
from parcelo.store import db


def _shipment(weight=4):
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, weight, "national")


def test_split_creates_one_shipment_per_weight():
    original = _shipment()
    parts = shipments.split_shipment(original.id, [1.5, 2.5])
    assert [p.weight_kg for p in parts] == [1.5, 2.5]
    for part in parts:
        assert part.customer_id == original.customer_id
        assert part.zone == original.zone
        assert part.status == "created"
        assert db.shipments[part.id] is part
    assert len({p.id for p in parts}) == 2


def test_split_marks_original():
    original = _shipment()
    shipments.split_shipment(original.id, [1, 1, 2])
    assert shipments.get_shipment(original.id).status == "split"


def test_split_missing_fails():
    with pytest.raises(Exception):
        shipments.split_shipment("nope", [1, 1])


def test_split_non_created_fails():
    original = _shipment()
    shipments.split_shipment(original.id, [2, 2])
    with pytest.raises(Exception):
        shipments.split_shipment(original.id, [2, 2])


def test_split_weights_must_add_up():
    original = _shipment()
    count = len(db.shipments)
    with pytest.raises(Exception):
        shipments.split_shipment(original.id, [1, 2])
    assert len(db.shipments) == count
    assert original.status == "created"
