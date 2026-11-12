import pytest

from parcelo import customers, shipments
from parcelo.errors import DomainError


def test_list_is_sorted_by_id():
    acme = customers.add_customer("Acme")
    made = [shipments.create_shipment(acme.id, 2, "local").id for _ in range(3)]
    assert [s.id for s in shipments.list_shipments(acme.id)] == sorted(made)


def test_unknown_customer():
    with pytest.raises(DomainError):
        shipments.list_shipments("nope")
