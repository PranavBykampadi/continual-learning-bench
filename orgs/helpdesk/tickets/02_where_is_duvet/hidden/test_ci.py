from checks import (
    assert_closed, assert_credit_given, assert_email_changed, assert_refunded_or_escalated, assert_reply,
)

CASE = "CS-4102"


def test_reply_addresses_the_case():
    assert_reply(CASE, ['MP-20102', 'NL-884201', 'tracking'])


def test_case_closed():
    assert_closed(CASE)
