import pytest

from checks import dollars
from parcelo import rates


def test_light_parcel_gets_normal_quote():
    assert dollars(rates.heavy_quote(2, "local")) == pytest.approx(7.0)


def test_exactly_thirty_kg_has_no_surcharge():
    assert dollars(rates.heavy_quote(30, "national")) == pytest.approx(rates.quote(30, "national"))


def test_heavy_parcel_pays_per_extra_kg():
    assert dollars(rates.heavy_quote(40, "local")) == pytest.approx(62.0)


def test_bad_zone_fails():
    with pytest.raises(Exception):
        rates.heavy_quote(40, "moon")


def test_bad_weight_fails():
    with pytest.raises(Exception):
        rates.heavy_quote(0, "local")
