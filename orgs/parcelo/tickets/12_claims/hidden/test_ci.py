import pytest

from checks import dollars
from parcelo import claims, customers, shipments
from parcelo.store import db


def _shipment(status="delivered"):
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    shipment.status = status
    return shipment


def test_file_claim_stores_claim():
    shipment = _shipment()
    claim = claims.file_claim(shipment.id, 12.5, "box crushed")
    assert claim.shipment_id == shipment.id
    assert claim.reason == "box crushed"
    assert dollars(claim.amount) == pytest.approx(12.5)
    assert claim.filed_at is not None
    assert db.claims[claim.id] is claim


def test_claims_get_distinct_ids():
    shipment = _shipment()
    first = claims.file_claim(shipment.id, 5, "late")
    second = claims.file_claim(shipment.id, 6, "damaged")
    assert first.id != second.id
    assert len(db.claims) == 2


def test_missing_shipment_fails():
    with pytest.raises(Exception):
        claims.file_claim("nope", 5, "late")


def test_undelivered_shipment_fails():
    shipment = _shipment("created")
    with pytest.raises(Exception):
        claims.file_claim(shipment.id, 5, "late")
    assert not db.claims


def test_non_positive_amount_fails():
    shipment = _shipment()
    with pytest.raises(Exception):
        claims.file_claim(shipment.id, 0, "late")
    with pytest.raises(Exception):
        claims.file_claim(shipment.id, -3, "late")
