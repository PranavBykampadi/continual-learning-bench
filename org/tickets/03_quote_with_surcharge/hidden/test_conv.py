import pytest

from checks import assert_new_unit_test, assert_no_legacy_imports
from parcelo import rates
from parcelo.errors import DomainError
from parcelo.money import Money


def test_conv_money():
    assert isinstance(rates.quote_with_surcharge(2, "national"), Money)


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_errors():
    with pytest.raises(DomainError):
        rates.quote_with_surcharge(2, "moon")
    with pytest.raises(DomainError):
        rates.quote_with_surcharge(0, "local")


def test_conv_tests():
    assert_new_unit_test()
