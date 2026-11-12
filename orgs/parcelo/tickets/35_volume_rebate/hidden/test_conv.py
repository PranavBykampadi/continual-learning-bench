import pytest

from checks import assert_changelog_v2, assert_no_legacy_imports, assert_settings
from parcelo import customers, shipments
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.money import Money
from parcelo.store import db


def _customer(count):
    customer = customers.add_customer("Acme")
    made = [shipments.create_shipment(customer.id, 1, "local") for _ in range(count)]
    db.invoices["INV-p"] = Invoice(id="INV-p", shipment_id=made[0].id, amount=200.0, status="paid")
    return customer


def test_conv_money():
    assert isinstance(customers.rebate_for(_customer(10).id), Money)
    assert isinstance(customers.rebate_for(customers.add_customer("Globex").id), Money)


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_settings():
    assert_settings("parcelo/customers.py", "rebate_for", [(10,), (50,), (0.03, 3), (0.06, 6)])


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.rebate_for("nope")


def test_conv_changelog2():
    assert_changelog_v2("PRC-161")
