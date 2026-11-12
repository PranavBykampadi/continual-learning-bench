import copy

import pytest

from checks import assert_api_doc, assert_changelog
from parcelo import audit, customers, events, shipments
from parcelo.errors import DomainError


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_conv_events():
    shipment = _shipment()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    shipments.mark_lost(shipment.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == shipment.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.mark_lost("nope")
    shipment = _shipment()
    shipment.status = "delivered"
    with pytest.raises(DomainError):
        shipments.mark_lost(shipment.id)


def test_conv_idempotent():
    shipment = _shipment()
    first = shipments.mark_lost(shipment.id)
    snapshot = copy.deepcopy(first)
    emitted = len(events.OUTBOX)
    again = shipments.mark_lost(shipment.id)
    assert again.id == shipment.id
    assert again == snapshot
    assert len(events.OUTBOX) == emitted


def test_conv_docs_api():
    assert_api_doc("shipments.mark_lost")


def test_conv_changelog():
    assert_changelog("PRC-152")
