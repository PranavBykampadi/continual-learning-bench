from checks import assert_api_doc, assert_changelog_v2, assert_new_unit_test
from parcelo import customers, reports
from parcelo.models import Invoice, Shipment
from parcelo.store import db


def test_conv_sorted():
    acme = customers.add_customer("Acme")
    for shipment_id in ("shp_000008", "shp_000003", "shp_000006", "shp_000001"):
        db.shipments[shipment_id] = Shipment(id=shipment_id, customer_id=acme.id, weight_kg=1, zone="local")
    db.invoices["INV-x"] = Invoice(id="INV-x", shipment_id="shp_000001", amount=5.0)
    found = [s.id for s in reports.shipments_without_invoice()]
    assert found == ["shp_000003", "shp_000006", "shp_000008"]


def test_conv_docs_api():
    assert_api_doc("reports.shipments_without_invoice")


def test_conv_changelog2():
    assert_changelog_v2("PRC-165")


def test_conv_tests():
    assert_new_unit_test()
