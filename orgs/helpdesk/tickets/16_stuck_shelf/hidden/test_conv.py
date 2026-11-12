from checks import assert_credit_cap, assert_no_delivery_promise, assert_one_tag, assert_signoff

CASE = "CS-4116"


def test_conv_credit_cap():
    assert_credit_cap(CASE)


def test_conv_no_dates():
    assert_no_delivery_promise(CASE)


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
