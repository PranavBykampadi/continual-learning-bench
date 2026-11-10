from parcelo import customers, invoices, reports, shipments


def test_outstanding():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoices.issue_invoice(shipment.id)
    assert reports.outstanding_by_customer()[customer.id].cents == 700
