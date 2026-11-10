from datetime import datetime, timedelta

from parcelo import customers, invoices, shipments


def test_late_fee():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    invoice = invoices.issue_invoice(shipment.id)
    invoice.issued_at = datetime.utcnow() - timedelta(days=40, hours=12)
    assert invoices.late_fee_for(invoice.id).cents == 105
