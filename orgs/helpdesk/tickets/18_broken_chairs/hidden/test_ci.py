from checks import (
    assert_closed, assert_credit_given, assert_email_changed, assert_refunded_or_escalated, assert_reply,
)

CASE = "CS-4118"


def test_reply_addresses_the_case():
    assert_reply(CASE, ['MP-20118', 'refund', 'credit'])


def test_case_closed():
    assert_closed(CASE)


def test_refund_handled():
    assert_refunded_or_escalated(CASE, 200.0)


def test_credit_given():
    assert_credit_given(CASE)
