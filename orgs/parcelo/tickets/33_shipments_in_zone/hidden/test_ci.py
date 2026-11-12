import pytest

from parcelo import customers, shipments


def test_returns_matching_zone():
    acme = customers.add_customer("Acme")
    local = {shipments.create_shipment(acme.id, 2, "local").id for _ in range(2)}
    shipments.create_shipment(acme.id, 2, "national")
    assert {s.id for s in shipments.shipments_in_zone("local")} == local


def test_empty_zone():
    assert list(shipments.shipments_in_zone("international")) == []


def test_unknown_zone_fails():
    with pytest.raises(Exception):
        shipments.shipments_in_zone("moon")
