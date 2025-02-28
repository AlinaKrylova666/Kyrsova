import pytest
import json
from datetime import datetime
from unittest.mock import patch
from src.views import get_greeting, get_currency_rates, get_stock_prices, generate_report

def test_get_greeting():
    morning = datetime.strptime("2023-11-01 08:00:00", "%Y-%m-%d %H:%M:%S")
    afternoon = datetime.strptime("2023-11-01 14:00:00", "%Y-%m-%d %H:%M:%S")
    evening = datetime.strptime("2023-11-01 19:00:00", "%Y-%m-%d %H:%M:%S")
    night = datetime.strptime("2023-11-01 23:00:00", "%Y-%m-%d %H:%M:%S")

    assert get_greeting(morning) == "Доброе утро"
    assert get_greeting(afternoon) == "Добрый день"
    assert get_greeting(evening) == "Добрый вечер"
    assert get_greeting(night) == "Доброй ночи"

@patch('src.views.requests.get')
def test_get_currency_rates(mock_get):
    mock_response = {
        "USD": {"rate": 74.0},
        "EUR": {"rate": 88.0}
    }
    mock_get.return_value.json.return_value = mock_response

    currencies = ["USD", "EUR"]
    rates = get_currency_rates(currencies)
    assert rates == {"USD": 74.0, "EUR": 88.0}

@patch('src.views.requests.get')
def test_get_stock_prices(mock_get):
    mock_response = {
        "AAPL": {"price": 150.0},
        "GOOGL": {"price": 2800.0}
    }
    mock_get.return_value.json.return_value = mock_response

    stocks = ["AAPL", "GOOGL"]
    prices = get_stock_prices(stocks)
    assert prices == {"AAPL": 150.0, "GOOGL": 2800.0}

@patch('src.views.get_currency_rates')
@patch('src.views.get_stock_prices')
@patch('src.views.load_user_settings')
def test_generate_report(mock_load_user_settings, mock_get_stock_prices, mock_get_currency_rates):
    mock_load_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "GOOGL"]
    }
    mock_get_currency_rates.return_value = {"USD": 74.0, "EUR": 88.0}
    mock_get_stock_prices.return_value = {"AAPL": 150.0, "GOOGL": 2800.0}

    result = json.loads(generate_report("2023-11-01 14:30:00"))

    assert result["greeting"] == "Добрый день"
    assert result["currency_rates"] == {"USD": 74.0, "EUR": 88.0}
    assert result["stock_prices"] == {"AAPL": 150.0, "GOOGL": 2800.0}

# Запуск тестов через командную строку
if __name__ == "__main__":
    pytest.main()
