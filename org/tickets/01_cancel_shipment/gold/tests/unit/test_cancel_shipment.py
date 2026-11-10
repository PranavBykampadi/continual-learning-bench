from parcelo import customers, shipments


def test_cancel():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    assert shipments.cancel_shipment(shipment.id, "late").status == "cancelled"
