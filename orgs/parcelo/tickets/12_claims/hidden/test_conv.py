import re
from datetime import datetime, timezone

import pytest

from checks import assert_no_direct_time, assert_no_uuid
from parcelo import audit, claims, clock, customers, shipments
from parcelo.errors import DomainError
from parcelo.money import Money


def _shipment(status="delivered"):
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = status
    return shipment


def test_conv_ids():
    claim = claims.file_claim(_shipment().id, 5, "late")
    assert re.match(r"^[a-z]+_\d{6}$", claim.id)
    assert_no_uuid("parcelo/claims.py", "file_claim")


def test_conv_money():
    claim = claims.file_claim(_shipment().id, 12.5, "late")
    assert isinstance(claim.amount, Money)
    assert claim.amount.cents == 1250


def test_conv_clock():
    fixed = datetime(2026, 3, 4, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    claim = claims.file_claim(_shipment().id, 5, "late")
    assert claim.filed_at == fixed
    assert_no_direct_time("parcelo/claims.py", "file_claim")


def test_conv_audit():
    shipment = _shipment()
    before = len(audit.LOG)
    claim = claims.file_claim(shipment.id, 5, "late")
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == claim.id


def test_conv_errors():
    with pytest.raises(DomainError):
        claims.file_claim("nope", 5, "late")
    with pytest.raises(DomainError):
        claims.file_claim(_shipment("created").id, 5, "late")
    with pytest.raises(DomainError):
        claims.file_claim(_shipment().id, 0, "late")
