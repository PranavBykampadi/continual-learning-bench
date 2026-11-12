import pytest

from checks import assert_api_doc, assert_changelog_v2, assert_new_unit_test
from parcelo import customers, shipments
from parcelo.errors import DomainError
from parcelo.models import Shipment
from parcelo.store import db


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.shipments_in_zone("moon")


def test_conv_sorted():
    acme = customers.add_customer("Acme")
    for shipment_id in ("shp_000007", "shp_000003", "shp_000004"):
        db.shipments[shipment_id] = Shipment(id=shipment_id, customer_id=acme.id, weight_kg=1, zone="national")
    db.shipments["shp_000001"] = Shipment(id="shp_000001", customer_id=acme.id, weight_kg=1, zone="local")
    found = [s.id for s in shipments.shipments_in_zone("national")]
    assert found == ["shp_000003", "shp_000004", "shp_000007"]


def test_conv_docs_api():
    assert_api_doc("shipments.shipments_in_zone")


def test_conv_changelog2():
    assert_changelog_v2("PRC-159")


def test_conv_tests():
    assert_new_unit_test()
