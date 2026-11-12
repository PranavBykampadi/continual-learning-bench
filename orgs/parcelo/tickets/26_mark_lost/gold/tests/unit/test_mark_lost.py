import pytest

from parcelo import customers, events, shipments
from parcelo.errors import DomainError


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_mark_lost():
    shipment = _shipment()
    assert shipments.mark_lost(shipment.id).status == "lost"
    assert events.OUTBOX[-1]["name"] == "shipment.lost"


def test_mark_lost_twice_is_a_noop():
    shipment = _shipment()
    shipments.mark_lost(shipment.id)
    emitted = len(events.OUTBOX)
    assert shipments.mark_lost(shipment.id).status == "lost"
    assert len(events.OUTBOX) == emitted


def test_delivered_cannot_be_lost():
    shipment = _shipment()
    shipment.status = "delivered"
    with pytest.raises(DomainError):
        shipments.mark_lost(shipment.id)
