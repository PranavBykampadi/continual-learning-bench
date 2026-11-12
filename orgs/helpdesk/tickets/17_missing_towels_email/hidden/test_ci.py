from checks import (
    assert_closed, assert_credit_given, assert_email_changed, assert_refunded_or_escalated, assert_reply,
)

CASE = "CS-4117"


def test_reply_addresses_the_case():
    assert_reply(CASE, ['MP-20117', 'refund', 'email'])


def test_case_closed():
    assert_closed(CASE)


def test_refund_handled():
    assert_refunded_or_escalated(CASE, 30.0)


def test_email_changed():
    assert_email_changed('C-1017', 'mia.schneider@example.net')
