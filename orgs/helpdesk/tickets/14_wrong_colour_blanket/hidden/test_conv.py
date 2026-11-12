from checks import assert_escalated_not_refunded, assert_greeting, assert_no_delivery_promise, assert_one_tag, assert_signoff

CASE = "CS-4114"


def test_conv_escalate_finance():
    assert_escalated_not_refunded(CASE, 'finance-ops')


def test_conv_greeting():
    assert_greeting(CASE, 'es-MX')


def test_conv_no_dates():
    assert_no_delivery_promise(CASE)


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
