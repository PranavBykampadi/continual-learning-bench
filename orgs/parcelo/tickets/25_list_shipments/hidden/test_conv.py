import pytest

from checks import assert_api_doc, assert_changelog, assert_new_unit_test
from parcelo import customers, shipments
from parcelo.errors import DomainError
from parcelo.models import Shipment
from parcelo.store import db


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.list_shipments("nope")


def test_conv_sorted():
    acme = customers.add_customer("Acme")
    globex = customers.add_customer("Globex")
    for shipment_id in ("shp_000009", "shp_000002", "shp_000005"):
        db.shipments[shipment_id] = Shipment(id=shipment_id, customer_id=acme.id, weight_kg=1, zone="local")
    db.shipments["shp_000001"] = Shipment(id="shp_000001", customer_id=globex.id, weight_kg=1, zone="local")
    found = [s.id for s in shipments.list_shipments(acme.id)]
    assert found == ["shp_000002", "shp_000005", "shp_000009"]


def test_conv_docs_api():
    assert_api_doc("shipments.list_shipments")


def test_conv_changelog():
    assert_changelog("PRC-151")


def test_conv_tests():
    assert_new_unit_test()
