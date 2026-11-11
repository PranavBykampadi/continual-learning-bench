import pytest

from checks import dollars
from parcelo import rates


def test_gold_discount():
    assert dollars(rates.discounted_quote(2, "local", "gold")) == pytest.approx(6.3)
    assert dollars(rates.discounted_quote(4, "international", "gold")) == pytest.approx(26.1)
    assert dollars(rates.discounted_quote(2, "national", "gold")) == pytest.approx(10.35)


def test_standard_has_no_discount():
    assert dollars(rates.discounted_quote(2, "local", "standard")) == pytest.approx(7.0)
    assert dollars(rates.discounted_quote(4, "international", "standard")) == pytest.approx(29.0)


def test_unknown_zone_fails():
    with pytest.raises(Exception):
        rates.discounted_quote(2, "moon", "gold")


def test_unknown_tier_fails():
    with pytest.raises(Exception):
        rates.discounted_quote(2, "local", "platinum")
