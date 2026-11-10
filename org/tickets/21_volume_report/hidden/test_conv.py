from checks import assert_changelog, assert_new_unit_test, assert_no_legacy_imports


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_changelog():
    assert_changelog("PRC-147")


def test_conv_tests():
    assert_new_unit_test()
