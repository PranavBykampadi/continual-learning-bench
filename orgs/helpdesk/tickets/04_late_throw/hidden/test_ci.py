from checks import (
    assert_closed, assert_credit_given, assert_email_changed, assert_refunded_or_escalated, assert_reply,
)

CASE = "CS-4104"


def test_reply_addresses_the_case():
    assert_reply(CASE, ['MP-20104', 'credit', 'tracking'])


def test_case_closed():
    assert_closed(CASE)


def test_credit_given():
    assert_credit_given(CASE)
