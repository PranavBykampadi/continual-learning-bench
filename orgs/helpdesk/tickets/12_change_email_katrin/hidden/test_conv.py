from checks import assert_greeting, assert_one_tag, assert_signoff, assert_verified_before_email_change

CASE = "CS-4112"


def test_conv_identity():
    assert_verified_before_email_change(CASE)


def test_conv_greeting():
    assert_greeting(CASE, 'de-DE')


def test_conv_tag():
    assert_one_tag(CASE)


def test_conv_signoff():
    assert_signoff(CASE)
