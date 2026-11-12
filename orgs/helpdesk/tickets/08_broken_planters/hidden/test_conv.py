from checks import assert_credit_cap, assert_escalated_not_refunded, assert_greeting, assert_one_tag, assert_signoff

CASE = "CS-4108"


def test_conv_escalate():
    assert_escalated_not_refunded(CASE, 'billing-review')


def test_conv_credit_cap():
    assert_credit_cap(CASE)


def test_conv_greeting():
    assert_greeting(CASE, 'es-MX')


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
