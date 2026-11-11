import pytest

from parcelo import customers, shipments
from parcelo.errors import DomainError


def test_add_note():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    result = shipments.add_note(shipment.id, "left at door")
    assert result.notes[-1]["text"] == "left at door"


def test_empty_note_rejected():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    with pytest.raises(DomainError):
        shipments.add_note(shipment.id, "")
