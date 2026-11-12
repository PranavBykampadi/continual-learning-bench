import pytest

from checks import assert_api_doc, assert_changelog
from parcelo import customers
from parcelo.errors import DomainError
from parcelo.models import Customer
from parcelo.store import db


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.customers_by_tier("platinum")


def test_conv_sorted():
    for customer_id in ("C0003", "C0001", "C0002"):
        db.customers[customer_id] = Customer(id=customer_id, name=customer_id, tier="gold")
    db.customers["C0000"] = Customer(id="C0000", name="plain")
    found = [c.id for c in customers.customers_by_tier("gold")]
    assert found == ["C0001", "C0002", "C0003"]


def test_conv_docs_api():
    assert_api_doc("customers.customers_by_tier")


def test_conv_changelog():
    assert_changelog("PRC-155")
