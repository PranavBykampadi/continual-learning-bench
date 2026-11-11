import pytest

from parcelo import rates


def test_gold_gets_ten_percent_off():
    assert rates.discounted_quote(2, "local", "gold") == 6.3


def test_standard_unchanged():
    assert rates.discounted_quote(2, "local", "standard") == 7.0


def test_unknown_tier():
    with pytest.raises(ValueError):
        rates.discounted_quote(2, "local", "platinum")
