import pytest

from parcelo import customers, events, shipments
from parcelo.errors import DomainError


def test_create_emits_event():
    c = customers.add_customer("Acme")
    s = shipments.create_shipment(c.id, 1.5, "national")
    assert s.id.startswith("shp_")
    assert events.OUTBOX[-1]["name"] == "shipment.created"


def test_unknown_customer():
    with pytest.raises(DomainError) as err:
        shipments.create_shipment("nope", 1, "local")
    assert err.value.code == "E_UNKNOWN_CUSTOMER"
