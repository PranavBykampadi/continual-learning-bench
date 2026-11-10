import pytest

from checks import dollars
from parcelo import rates


def test_local_is_two_percent():
    assert dollars(rates.insurance_fee(200, "local")) == pytest.approx(4.0)


def test_national_adds_fuel_surcharge():
    assert dollars(rates.insurance_fee(100, "national")) == pytest.approx(6.0)


def test_international_adds_fuel_surcharge():
    assert dollars(rates.insurance_fee(200, "international")) == pytest.approx(23.0)


def test_minimum_fee():
    assert dollars(rates.insurance_fee(10, "local")) == pytest.approx(1.0)
    assert dollars(rates.insurance_fee(30, "national")) == pytest.approx(1.8)


def test_unknown_zone_fails():
    with pytest.raises(Exception):
        rates.insurance_fee(100, "moon")


def test_non_positive_value_fails():
    with pytest.raises(Exception):
        rates.insurance_fee(0, "local")
    with pytest.raises(Exception):
        rates.insurance_fee(-5, "local")
