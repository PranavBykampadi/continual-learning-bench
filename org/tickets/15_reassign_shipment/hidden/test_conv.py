import pytest

from checks import assert_changelog, assert_new_unit_test
from parcelo import audit, customers, events, shipments
from parcelo.errors import DomainError


def _setup():
    first = customers.add_customer("Acme")
    second = customers.add_customer("Globex")
    return first, second, shipments.create_shipment(first.id, 2, "local")


def test_conv_events():
    _, second, shipment = _setup()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    shipments.reassign_shipment(shipment.id, second.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == shipment.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    first, second, shipment = _setup()
    with pytest.raises(DomainError):
        shipments.reassign_shipment("nope", second.id)
    with pytest.raises(DomainError):
        shipments.reassign_shipment(shipment.id, "nope")
    shipment.status = "delivered"
    with pytest.raises(DomainError):
        shipments.reassign_shipment(shipment.id, second.id)


def test_conv_changelog():
    assert_changelog("PRC-141")


def test_conv_tests():
    assert_new_unit_test()
