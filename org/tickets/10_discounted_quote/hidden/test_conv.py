import pytest

from checks import assert_changelog, assert_no_legacy_imports
from parcelo import rates
from parcelo.errors import DomainError
from parcelo.money import Money


def test_conv_money():
    assert isinstance(rates.discounted_quote(2, "local", "gold"), Money)
    assert isinstance(rates.discounted_quote(2, "local", "standard"), Money)


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_errors():
    with pytest.raises(DomainError):
        rates.discounted_quote(2, "moon", "gold")
    with pytest.raises(DomainError):
        rates.discounted_quote(2, "local", "platinum")


def test_conv_changelog():
    assert_changelog("PRC-110")
