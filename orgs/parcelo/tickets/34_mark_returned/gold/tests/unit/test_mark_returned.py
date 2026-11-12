import pytest

from parcelo import customers, events, shipments
from parcelo.errors import DomainError


def _shipment(status):
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = status
    return shipment


def test_mark_returned():
    shipment = _shipment("delivered")
    result = shipments.mark_returned(shipment.id)
    assert result.status == "returned"
    assert result.returned_at is not None
    assert events.OUTBOX[-1]["name"] == "shipment.returned"


def test_second_call_is_a_noop():
    shipment = _shipment("delivered")
    first = shipments.mark_returned(shipment.id).returned_at
    emitted = len(events.OUTBOX)
    assert shipments.mark_returned(shipment.id).returned_at == first
    assert len(events.OUTBOX) == emitted


def test_created_cannot_be_returned():
    shipment = _shipment("created")
    with pytest.raises(DomainError):
        shipments.mark_returned(shipment.id)
