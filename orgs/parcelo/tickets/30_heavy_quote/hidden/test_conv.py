import pytest

from checks import assert_api_doc, assert_changelog, assert_settings
from parcelo import rates
from parcelo.errors import DomainError
from parcelo.money import Money


def test_conv_money():
    assert isinstance(rates.heavy_quote(2, "local"), Money)
    assert isinstance(rates.heavy_quote(40, "local"), Money)


def test_conv_settings():
    assert_settings("parcelo/rates.py", "heavy_quote", [(30,), (0.75, 75)])


def test_conv_errors():
    with pytest.raises(DomainError):
        rates.heavy_quote(40, "moon")
    with pytest.raises(DomainError):
        rates.heavy_quote(0, "local")


def test_conv_docs_api():
    assert_api_doc("rates.heavy_quote")


def test_conv_changelog():
    assert_changelog("PRC-156")
