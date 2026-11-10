from checks import assert_changelog, assert_new_unit_test
from parcelo import customers, invoices, reports, shipments
from parcelo.money import Money


def test_conv_money():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoices.issue_invoice(shipment.id)
    result = reports.outstanding_by_customer()
    assert isinstance(result[customer.id], Money)


def test_conv_changelog():
    assert_changelog("PRC-108")


def test_conv_tests():
    assert_new_unit_test()
