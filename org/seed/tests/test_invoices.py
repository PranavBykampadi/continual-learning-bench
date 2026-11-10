from parcelo import customers, invoices, shipments


def test_issue_and_pay():
    c = customers.add_customer("Acme")
    s = shipments.create_shipment(c.id, 2, "local")
    inv = invoices.issue_invoice(s.id)
    assert inv.amount == 7.0
    assert invoices.mark_paid(inv.id).status == "paid"
