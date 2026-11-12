import pytest

from parcelo import customers, events, settings, vouchers
from parcelo.errors import DomainError
from parcelo.money import Money


def test_issue_voucher():
    customer = customers.add_customer("Acme")
    voucher = vouchers.issue_voucher(customer.id, 20)
    assert voucher.id.startswith("vch_")
    assert voucher.amount == Money(2000)
    assert events.OUTBOX[-1]["name"] == "voucher.issued"


def test_over_the_maximum():
    customer = customers.add_customer("Acme")
    with pytest.raises(DomainError):
        vouchers.issue_voucher(customer.id, settings.MAX_VOUCHER + 1)


def test_bad_amount_and_customer():
    customer = customers.add_customer("Acme")
    with pytest.raises(DomainError):
        vouchers.issue_voucher(customer.id, 0)
    with pytest.raises(DomainError):
        vouchers.issue_voucher("nope", 10)
