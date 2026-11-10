import pytest

from checks import dollars
from parcelo import rates


def test_local_has_no_surcharge():
    assert dollars(rates.quote_with_surcharge(2, "local")) == pytest.approx(7.0)


def test_national_surcharge():
    assert dollars(rates.quote_with_surcharge(2, "national")) == pytest.approx(11.96)


def test_international_surcharge():
    assert dollars(rates.quote_with_surcharge(2, "international")) == pytest.approx(29.02)


def test_unknown_zone_fails():
    with pytest.raises(Exception):
        rates.quote_with_surcharge(2, "moon")


def test_bad_weight_fails():
    with pytest.raises(Exception):
        rates.quote_with_surcharge(0, "local")
    with pytest.raises(Exception):
        rates.quote_with_surcharge(-1, "local")
