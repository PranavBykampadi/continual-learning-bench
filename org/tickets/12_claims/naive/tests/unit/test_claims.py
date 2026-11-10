import pytest

from parcelo import claims, customers, shipments


def _delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = "delivered"
    return shipment


def test_file_claim():
    claim = claims.file_claim(_delivered().id, 12.5, "box crushed")
    assert claim.amount == 12.5


def test_undelivered_rejected():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    with pytest.raises(ValueError):
        claims.file_claim(shipment.id, 5, "late")


def test_non_positive_amount_rejected():
    with pytest.raises(ValueError):
        claims.file_claim(_delivered().id, 0, "late")
