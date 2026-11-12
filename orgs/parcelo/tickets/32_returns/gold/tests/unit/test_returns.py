import pytest

from parcelo import customers, events, returns, shipments, settings
from parcelo.errors import DomainError


def _delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = "delivered"
    return shipment


def test_request_return():
    shipment = _delivered()
    request = returns.request_return(shipment.id, "damaged")
    assert request.id.startswith("ret_")
    assert events.OUTBOX[-1]["name"] == "return.requested"


def test_returns_for_is_sorted():
    shipment = _delivered()
    made = [returns.request_return(shipment.id, "x").id for _ in range(3)]
    assert [r.id for r in returns.returns_for(shipment.id)] == sorted(made)


def test_limit():
    shipment = _delivered()
    for _ in range(settings.MAX_RETURN_REQUESTS):
        returns.request_return(shipment.id, "x")
    with pytest.raises(DomainError):
        returns.request_return(shipment.id, "x")


def test_only_delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    with pytest.raises(DomainError):
        returns.request_return(shipment.id, "x")
