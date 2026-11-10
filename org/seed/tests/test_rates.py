import pytest

from parcelo import rates


def test_quote_local():
    assert rates.quote(2, "local") == 7.0


def test_unknown_zone():
    with pytest.raises(ValueError):
        rates.base_rate("moon")
