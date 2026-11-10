import pytest

from parcelo import rates


def test_national_surcharge():
    assert rates.quote_with_surcharge(2, "national").cents == 1196


def test_unknown_zone():
    with pytest.raises(Exception):
        rates.quote_with_surcharge(2, "moon")
