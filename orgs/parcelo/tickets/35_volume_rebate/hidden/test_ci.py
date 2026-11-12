import pytest

from checks import dollars
from parcelo import customers, shipments
from parcelo.models import Invoice
from parcelo.store import db


def _customer(count, paid=200.0, open_amount=0.0):
    customer = customers.add_customer("Acme")
    made = [shipments.create_shipment(customer.id, 1, "local") for _ in range(count)]
    db.invoices["INV-p"] = Invoice(id="INV-p", shipment_id=made[0].id, amount=paid, status="paid")
    if open_amount:
        db.invoices["INV-o"] = Invoice(id="INV-o", shipment_id=made[0].id, amount=open_amount)
    return customer


def test_no_rebate_under_ten_shipments():
    assert dollars(customers.rebate_for(_customer(9).id)) == 0


def test_three_percent_from_ten_shipments():
    assert dollars(customers.rebate_for(_customer(10).id)) == pytest.approx(6.0)


def test_six_percent_from_fifty_shipments():
    assert dollars(customers.rebate_for(_customer(50).id)) == pytest.approx(12.0)


def test_open_invoices_do_not_count():
    assert dollars(customers.rebate_for(_customer(10, open_amount=1000.0).id)) == pytest.approx(6.0)


def test_unknown_customer_fails():
    with pytest.raises(Exception):
        customers.rebate_for("nope")
