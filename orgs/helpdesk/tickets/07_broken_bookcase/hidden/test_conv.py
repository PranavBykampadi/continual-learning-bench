from checks import assert_escalated_not_refunded, assert_no_delivery_promise, assert_one_tag, assert_signoff

CASE = "CS-4107"


def test_conv_escalate():
    assert_escalated_not_refunded(CASE, 'billing-review')


def test_conv_no_dates():
    assert_no_delivery_promise(CASE)


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
