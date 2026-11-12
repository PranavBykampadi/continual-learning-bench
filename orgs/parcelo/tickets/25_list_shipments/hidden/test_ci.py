import pytest

from parcelo import customers, shipments


def test_lists_only_that_customers_shipments():
    acme = customers.add_customer("Acme")
    globex = customers.add_customer("Globex")
    mine = [shipments.create_shipment(acme.id, 2, "local").id for _ in range(3)]
    shipments.create_shipment(globex.id, 2, "local")
    assert {s.id for s in shipments.list_shipments(acme.id)} == set(mine)


def test_empty_list_for_customer_without_shipments():
    acme = customers.add_customer("Acme")
    assert list(shipments.list_shipments(acme.id)) == []


def test_unknown_customer_fails():
    with pytest.raises(Exception):
        shipments.list_shipments("nope")
