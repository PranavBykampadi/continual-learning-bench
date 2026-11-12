from parcelo import customers, invoices, reports, shipments


def test_lists_only_uninvoiced_shipments():
    acme = customers.add_customer("Acme")
    billed = shipments.create_shipment(acme.id, 2, "local")
    open_one = shipments.create_shipment(acme.id, 2, "national")
    invoices.issue_invoice(billed.id)
    assert {s.id for s in reports.shipments_without_invoice()} == {open_one.id}


def test_empty_when_everything_is_invoiced():
    acme = customers.add_customer("Acme")
    invoices.issue_invoice(shipments.create_shipment(acme.id, 2, "local").id)
    assert list(reports.shipments_without_invoice()) == []
