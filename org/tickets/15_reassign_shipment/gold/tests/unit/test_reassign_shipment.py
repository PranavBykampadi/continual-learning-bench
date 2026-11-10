import pytest

from parcelo import customers, events, shipments
from parcelo.errors import DomainError


def _setup():
    first = customers.add_customer("Acme")
    second = customers.add_customer("Globex")
    return second, shipments.create_shipment(first.id, 2, "local")


def test_reassign():
    second, shipment = _setup()
    assert shipments.reassign_shipment(shipment.id, second.id).customer_id == second.id
    assert events.OUTBOX[-1]["name"] == "shipment.reassigned"


def test_reassign_unknown_customer():
    _, shipment = _setup()
    with pytest.raises(DomainError):
        shipments.reassign_shipment(shipment.id, "nope")


def test_reassign_delivered():
    second, shipment = _setup()
    shipment.status = "delivered"
    with pytest.raises(DomainError):
        shipments.reassign_shipment(shipment.id, second.id)
