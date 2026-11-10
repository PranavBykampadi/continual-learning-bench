import pytest

from checks import assert_new_unit_test, assert_no_legacy_imports
from parcelo import rates
from parcelo.errors import DomainError
from parcelo.money import Money


def test_conv_money():
    assert isinstance(rates.insurance_fee(100, "national"), Money)


def test_conv_errors():
    with pytest.raises(DomainError):
        rates.insurance_fee(100, "moon")
    with pytest.raises(DomainError):
        rates.insurance_fee(0, "local")
    with pytest.raises(DomainError):
        rates.insurance_fee(-5, "local")


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_tests():
    assert_new_unit_test()
