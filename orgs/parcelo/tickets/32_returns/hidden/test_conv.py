import re
from datetime import datetime, timezone

import pytest

from checks import assert_no_direct_time, assert_no_uuid, assert_settings
from parcelo import audit, clock, customers, events, returns, shipments
from parcelo.errors import DomainError
from parcelo.models import ReturnRequest
from parcelo.store import db


def _delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = "delivered"
    return shipment


def test_conv_ids():
    request = returns.request_return(_delivered().id, "x")
    assert re.match(r"^[a-z]+_\d{6}$", request.id)
    assert_no_uuid("parcelo/returns.py", "request_return")


def test_conv_events():
    shipment = _delivered()
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    request = returns.request_return(shipment.id, "x")
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == request.id
    assert len(audit.LOG) == before_audit


def test_conv_clock():
    shipment = _delivered()
    fixed = datetime(2030, 1, 1, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    assert returns.request_return(shipment.id, "x").requested_at == fixed
    assert_no_direct_time("parcelo/returns.py", "request_return")


def test_conv_errors():
    with pytest.raises(DomainError):
        returns.request_return("nope", "x")
    customer = customers.add_customer("Globex")
    undelivered = shipments.create_shipment(customer.id, 2, "local")
    with pytest.raises(DomainError):
        returns.request_return(undelivered.id, "x")
    shipment = _delivered()
    for _ in range(3):
        returns.request_return(shipment.id, "x")
    with pytest.raises(DomainError):
        returns.request_return(shipment.id, "x")


def test_conv_sorted():
    shipment = _delivered()
    for request_id in ("ret_000009", "ret_000002", "ret_000005"):
        db.returns[request_id] = ReturnRequest(id=request_id, shipment_id=shipment.id, reason="x")
    db.returns["ret_000001"] = ReturnRequest(id="ret_000001", shipment_id="other", reason="x")
    found = [r.id for r in returns.returns_for(shipment.id)]
    assert found == ["ret_000002", "ret_000005", "ret_000009"]


def test_conv_settings():
    assert_settings("parcelo/returns.py", "request_return", [(3,)])
