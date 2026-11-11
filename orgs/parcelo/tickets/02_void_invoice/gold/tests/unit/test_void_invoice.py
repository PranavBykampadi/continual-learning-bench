from parcelo import customers, invoices, shipments


def test_void():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    assert invoices.void_invoice(invoice.id).status == "void"
