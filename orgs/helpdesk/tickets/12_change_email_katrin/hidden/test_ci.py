from checks import (
    assert_closed, assert_credit_given, assert_email_changed, assert_refunded_or_escalated, assert_reply,
)

CASE = "CS-4112"


def test_reply_addresses_the_case():
    assert_reply(CASE, ['katrin.vogel@example.net', 'email'])


def test_case_closed():
    assert_closed(CASE)


def test_email_changed():
    assert_email_changed('C-1012', 'katrin.vogel@example.net')
