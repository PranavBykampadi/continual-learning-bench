import pytest

from checks import dollars
from parcelo import customers, vouchers
from parcelo.store import db


def test_voucher_is_created_and_stored():
    customer = customers.add_customer("Acme")
    voucher = vouchers.issue_voucher(customer.id, 25.5)
    assert voucher.customer_id == customer.id
    assert dollars(voucher.amount) == pytest.approx(25.5)
    assert voucher.issued_at is not None
    assert db.vouchers[voucher.id] is voucher


def test_exactly_the_maximum_is_allowed():
    customer = customers.add_customer("Acme")
    assert dollars(vouchers.issue_voucher(customer.id, 150).amount) == pytest.approx(150.0)


def test_unknown_customer_fails():
    with pytest.raises(Exception):
        vouchers.issue_voucher("nope", 10)


def test_too_large_fails():
    customer = customers.add_customer("Acme")
    with pytest.raises(Exception):
        vouchers.issue_voucher(customer.id, 150.01)


@pytest.mark.parametrize("amount", [0, -5])
def test_non_positive_fails(amount):
    customer = customers.add_customer("Acme")
    with pytest.raises(Exception):
        vouchers.issue_voucher(customer.id, amount)
