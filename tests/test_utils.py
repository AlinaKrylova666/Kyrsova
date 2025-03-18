import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from src.utils import (load_user_settings, get_greeting, get_currency_rates,
                         get_stock_prices, collect_cards_data, get_top_transactions)

class TestFunctions(unittest.TestCase):
    @patch('builtins.open', new_callable=MagicMock)
    def test_load_user_settings(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = '{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}'
        settings = load_user_settings()
        self.assertEqual(settings, {"user_currencies": ["USD"], "user_stocks": ["AAPL"]})

    def test_get_greeting(self):
        self.assertEqual(get_greeting(datetime(2023, 1, 1, 6)), "Доброе утро")
        self.assertEqual(get_greeting(datetime(2023, 1, 1, 13)), "Добрый день")
        self.assertEqual(get_greeting(datetime(2023, 1, 1, 19)), "Добрый вечер")
        self.assertEqual(get_greeting(datetime(2023, 1, 1, 23)), "Доброй ночи")

    @patch('requests.get')
    def test_get_currency_rates(self, mock_get):
        mock_get.return_value.json.return_value = {'rates': {'RUB': 75.0}}
        rates = get_currency_rates(['USD'])
        self.assertEqual(rates, [{'currency': 'USD', 'rate': 75.0}])

    @patch('requests.get')
    def test_get_stock_prices(self, mock_get):
        mock_get.return_value.json.return_value = {
            "Time Series (1min)": {
                "2023-01-01 00:00:00": {"1. open": "150.0"}
            }
        }
        prices = get_stock_prices(['AAPL'])
        self.assertEqual(prices, {'AAPL': 150.0})

    def test_collect_cards_data(self):
        data = pd.DataFrame({
            'Номер карты': ['****1234', '****1234', '****5678'],
            'Сумма операции': [-100, -200, -50]
        })
        result = collect_cards_data(data)
        expected = [
            {'last_digits': '1234', 'total_spent': 300.0, 'cashback': 3.0},
            {'last_digits': '5678', 'total_spent': 50.0, 'cashback': 0.5}
        ]
        self.assertEqual(result, expected)

    def test_get_top_transactions(self):
        data = pd.DataFrame({
            'Сумма операции': [100, 200, 300, 400, 500, 600]
        })
        result = get_top_transactions(data)
        expected = pd.DataFrame({
            'Сумма операции': [600, 500, 400, 300, 200]
        }).reset_index(drop=True)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

if __name__ == '__main__':
    unittest.main()
