import pytest

from parcelo import rates
from parcelo.errors import DomainError


def test_gold_gets_ten_percent_off():
    assert rates.discounted_quote(2, "local", "gold").cents == 630


def test_standard_unchanged():
    assert rates.discounted_quote(2, "local", "standard").cents == 700


def test_unknown_tier():
    with pytest.raises(DomainError):
        rates.discounted_quote(2, "local", "platinum")
