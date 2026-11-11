import pytest

from parcelo import audit, customers, shipments
from parcelo.errors import DomainError


def test_create_records_audit():
    c = customers.add_customer("Acme")
    s = shipments.create_shipment(c.id, 1.5, "national")
    assert s.id.startswith("shp_")
    assert audit.LOG[-1]["action"] == "shipment.created"


def test_unknown_customer():
    with pytest.raises(DomainError) as err:
        shipments.create_shipment("nope", 1, "local")
    assert err.value.code == "E_UNKNOWN_CUSTOMER"
