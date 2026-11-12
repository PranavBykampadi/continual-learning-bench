from parcelo import customers, invoices, reports, shipments


def test_sorted_and_filtered():
    acme = customers.add_customer("Acme")
    made = [shipments.create_shipment(acme.id, 2, "local") for _ in range(3)]
    invoices.issue_invoice(made[1].id)
    assert [s.id for s in reports.shipments_without_invoice()] == sorted([made[0].id, made[2].id])
