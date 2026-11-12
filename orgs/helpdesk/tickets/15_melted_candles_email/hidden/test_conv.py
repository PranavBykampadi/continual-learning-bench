from checks import assert_escalated_not_refunded, assert_one_tag, assert_signoff, assert_verified_before_email_change

CASE = "CS-4115"


def test_conv_escalate_finance():
    assert_escalated_not_refunded(CASE, 'finance-ops')


def test_conv_identity():
    assert_verified_before_email_change(CASE)


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
