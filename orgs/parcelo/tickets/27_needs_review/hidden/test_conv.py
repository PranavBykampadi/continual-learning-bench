import pytest

from checks import assert_api_doc, assert_changelog, assert_new_unit_test, assert_settings
from parcelo import customers
from parcelo.errors import DomainError


def test_conv_errors():
    with pytest.raises(DomainError):
        customers.needs_review("nope")


def test_conv_settings():
    assert_settings("parcelo/customers.py", "needs_review", [(3,), (250, 25000)])


def test_conv_docs_api():
    assert_api_doc("customers.needs_review")


def test_conv_changelog():
    assert_changelog("PRC-153")


def test_conv_tests():
    assert_new_unit_test()
