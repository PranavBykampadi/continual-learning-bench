import pytest

from parcelo import rates, settings
from parcelo.errors import DomainError
from parcelo.money import Money


def test_light_parcel():
    assert rates.heavy_quote(2, "local") == Money(700)


def test_heavy_parcel():
    assert rates.heavy_quote(settings.HEAVY_KG + 10, "local") == Money.parse(rates.quote(40, "local")) + Money(750)


def test_bad_zone():
    with pytest.raises(DomainError):
        rates.heavy_quote(40, "moon")
