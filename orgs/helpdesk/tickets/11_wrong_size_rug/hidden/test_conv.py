from checks import assert_escalated_not_refunded, assert_greeting, assert_one_tag, assert_signoff

CASE = "CS-4111"


def test_conv_escalate_finance():
    assert_escalated_not_refunded(CASE, 'finance-ops')


def test_conv_greeting():
    assert_greeting(CASE, 'fr-FR')


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
