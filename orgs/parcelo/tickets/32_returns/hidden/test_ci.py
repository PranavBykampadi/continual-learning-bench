import pytest

from parcelo import customers, returns, shipments


def _delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = "delivered"
    return shipment


def test_request_is_created_and_stored():
    from parcelo.store import db

    shipment = _delivered()
    request = returns.request_return(shipment.id, "damaged")
    assert request.shipment_id == shipment.id
    assert request.reason == "damaged"
    assert request.requested_at is not None
    assert db.returns[request.id] is request


def test_returns_for_lists_requests():
    shipment = _delivered()
    made = {returns.request_return(shipment.id, "x").id for _ in range(2)}
    assert {r.id for r in returns.returns_for(shipment.id)} == made


def test_missing_shipment_fails():
    with pytest.raises(Exception):
        returns.request_return("nope", "x")


def test_undelivered_shipment_fails():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    with pytest.raises(Exception):
        returns.request_return(shipment.id, "x")


def test_fourth_request_fails():
    shipment = _delivered()
    for _ in range(3):
        returns.request_return(shipment.id, "x")
    with pytest.raises(Exception):
        returns.request_return(shipment.id, "x")
    assert len(returns.returns_for(shipment.id)) == 3
