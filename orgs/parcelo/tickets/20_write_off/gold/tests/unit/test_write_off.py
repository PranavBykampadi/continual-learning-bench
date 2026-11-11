from parcelo import customers, invoices, shipments


def test_write_off():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    invoices.write_off(invoice.id)
    assert invoice.status == "written_off"
    assert invoice.written_off_at is not None
