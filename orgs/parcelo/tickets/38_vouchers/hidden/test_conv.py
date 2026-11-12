import re

from checks import assert_api_doc, assert_changelog_v2, assert_no_uuid, assert_settings
from parcelo import audit, customers, events, vouchers
from parcelo.money import Money


def test_conv_ids():
    customer = customers.add_customer("Acme")
    voucher = vouchers.issue_voucher(customer.id, 10)
    assert re.match(r"^[a-z]+_\d{6}$", voucher.id)
    assert_no_uuid("parcelo/vouchers.py", "issue_voucher")


def test_conv_money():
    customer = customers.add_customer("Acme")
    assert isinstance(vouchers.issue_voucher(customer.id, 10).amount, Money)


def test_conv_settings():
    assert_settings("parcelo/vouchers.py", "issue_voucher", [(150, 15000)])


def test_conv_events():
    customer = customers.add_customer("Acme")
    before_events = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    voucher = vouchers.issue_voucher(customer.id, 10)
    assert len(events.OUTBOX) > before_events
    assert events.OUTBOX[-1]["entity_id"] == voucher.id
    assert len(audit.LOG) == before_audit


def test_conv_docs_api():
    assert_api_doc("vouchers.issue_voucher")


def test_conv_changelog2():
    assert_changelog_v2("PRC-164")
