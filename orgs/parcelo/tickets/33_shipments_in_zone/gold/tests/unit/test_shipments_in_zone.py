import pytest

from parcelo import customers, shipments
from parcelo.errors import DomainError


def test_in_zone_sorted():
    acme = customers.add_customer("Acme")
    made = [shipments.create_shipment(acme.id, 2, "national").id for _ in range(3)]
    shipments.create_shipment(acme.id, 2, "local")
    assert [s.id for s in shipments.shipments_in_zone("national")] == sorted(made)


def test_bad_zone():
    with pytest.raises(DomainError):
        shipments.shipments_in_zone("moon")
