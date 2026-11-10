import pytest

from parcelo import rates
from parcelo.errors import DomainError
from parcelo.money import Money


def test_fee_includes_fuel_surcharge():
    assert rates.insurance_fee(100, "national") == Money(600)


def test_fee_has_a_minimum():
    assert rates.insurance_fee(10, "local") == Money(100)


def test_bad_inputs():
    with pytest.raises(DomainError):
        rates.insurance_fee(100, "moon")
    with pytest.raises(DomainError):
        rates.insurance_fee(0, "local")
