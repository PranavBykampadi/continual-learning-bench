import pytest

from checks import assert_changelog, assert_new_unit_test
from parcelo import audit, customers, shipments
from parcelo.errors import DomainError


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_conv_errors():
    with pytest.raises(DomainError):
        shipments.cancel_shipment("nope", "x")
    shipment = _shipment()
    shipments.cancel_shipment(shipment.id, "x")
    with pytest.raises(DomainError):
        shipments.cancel_shipment(shipment.id, "x")


def test_conv_audit():
    shipment = _shipment()
    before = len(audit.LOG)
    shipments.cancel_shipment(shipment.id, "x")
    assert len(audit.LOG) > before
    assert audit.LOG[-1]["entity_id"] == shipment.id


def test_conv_changelog():
    assert_changelog("PRC-101")


def test_conv_tests():
    assert_new_unit_test()
