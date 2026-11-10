import pytest

from checks import dollars
from parcelo import customers, invoices, reports, shipments


def _invoice(customer, weight, zone):
    shipment = shipments.create_shipment(customer.id, weight, zone)
    return invoices.issue_invoice(shipment.id)


def test_totals_open_invoices_per_customer():
    acme = customers.add_customer("Acme")
    globex = customers.add_customer("Globex")
    _invoice(acme, 2, "local")
    _invoice(acme, 3, "national")
    paid = _invoice(globex, 2, "local")
    invoices.mark_paid(paid.id)
    result = reports.outstanding_by_customer()
    assert dollars(result[acme.id]) == pytest.approx(19.75)
    assert dollars(result.get(globex.id, 0)) == 0


def test_empty():
    assert reports.outstanding_by_customer() == {}
