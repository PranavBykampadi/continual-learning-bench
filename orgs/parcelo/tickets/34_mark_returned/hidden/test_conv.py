import copy
from datetime import datetime, timedelta, timezone

import pytest

from checks import assert_api_doc, assert_changelog_v2, assert_no_direct_time
from parcelo import audit, clock, customers, events, shipments
from parcelo.errors import DomainError


def _delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = "delivered"
    return shipment


def test_conv_events():
    shipment = _delivered()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    shipments.mark_returned(shipment.id)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == shipment.id
    assert len(audit.LOG) == before_audit


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.mark_returned("nope")
    customer = customers.add_customer("Globex")
    fresh = shipments.create_shipment(customer.id, 2, "local")
    with pytest.raises(DomainError):
        shipments.mark_returned(fresh.id)


def test_conv_clock():
    shipment = _delivered()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    assert shipments.mark_returned(shipment.id).returned_at == fixed
    assert_no_direct_time("parcelo/shipments.py", "mark_returned")


def test_conv_idempotent():
    shipment = _delivered()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    snapshot = copy.deepcopy(shipments.mark_returned(shipment.id))
    clock.set_fixed(fixed + timedelta(hours=3))
    emitted = len(events.OUTBOX)
    again = shipments.mark_returned(shipment.id)
    assert again.id == shipment.id
    assert again == snapshot
    assert len(events.OUTBOX) == emitted


def test_conv_docs_api():
    assert_api_doc("shipments.mark_returned")


def test_conv_changelog2():
    assert_changelog_v2("PRC-160")
