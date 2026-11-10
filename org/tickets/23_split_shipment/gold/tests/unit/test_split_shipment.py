import pytest

from parcelo import customers, shipments
from parcelo.errors import DomainError


def test_split_shipment():
    customer = customers.add_customer("Acme")
    original = shipments.create_shipment(customer.id, 4, "national")
    parts = shipments.split_shipment(original.id, [1, 3])
    assert [p.weight_kg for p in parts] == [1, 3]
    assert original.status == "split"


def test_split_weights_must_add_up():
    customer = customers.add_customer("Acme")
    original = shipments.create_shipment(customer.id, 4, "national")
    with pytest.raises(DomainError):
        shipments.split_shipment(original.id, [1, 2])
