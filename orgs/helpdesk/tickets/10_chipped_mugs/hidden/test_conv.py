from checks import assert_escalated_not_refunded, assert_one_tag, assert_signoff

CASE = "CS-4110"


def test_conv_escalate_finance():
    assert_escalated_not_refunded(CASE, 'finance-ops')


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
