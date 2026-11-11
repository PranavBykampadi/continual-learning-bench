from parcelo import customers, shipments


def test_mark_delivered():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    assert shipments.mark_delivered(shipment.id).status == "delivered"
