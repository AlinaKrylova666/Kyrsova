import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from src.views import generate_main_page

class TestGenerateMainPage(unittest.TestCase):
    @patch('src.utils.load_user_settings')
    @patch('src.utils.get_greeting')
    @patch('src.utils.get_currency_rates')
    @patch('src.utils.get_stock_prices')
    @patch('src.utils.collect_cards_data')
    @patch('src.utils.get_top_transactions')
    def test_generate_main_page(self, mock_top_transactions, mock_collect_cards_data,
                                mock_get_stock_prices, mock_get_currency_rates,
                                mock_get_greeting, mock_load_user_settings):
        # Настройка моков
        mock_load_user_settings.return_value = {'user_currencies': ['USD', 'EUR'], 'user_stocks': ['AAPL', 'GOOGL']}
        mock_get_greeting.return_value = 'Добрый день'
        mock_get_currency_rates.return_value = [
            {'currency': 'USD', 'rate': 85.85},
            {'currency': 'EUR', 'rate': 93.44}
        ]
        mock_get_stock_prices.return_value = {'AAPL': 213.26, 'GOOGL': 165.26}
        mock_collect_cards_data.return_value = [{'last_digits': '1234', 'total_spent': 300.0, 'cashback': 3.0}]
        mock_top_transactions.return_value = pd.DataFrame({'Сумма операции': [500, 400, 300, 200, 100]})

        transactions_df = pd.DataFrame({
            'Дата операции': ['01.09.2023', '15.09.2023', '05.10.2023', '01.10.2023'],
            'Сумма операции': [-100, -200, -150, -250],
            'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения'],
            'Номер карты': ['****1234', '****1234', '****5678', '****1234']
        })

        # Вызов тестируемой функции
        result = generate_main_page(transactions_df, '2023-10-15 12:00:00')

        # Проверка результатов
        self.assertEqual(result['greeting'], 'Добрый день')
        self.assertEqual(result['currency_rates'], [
            {'currency': 'USD', 'rate': 85.85},
            {'currency': 'EUR', 'rate': 93.44}
        ])
        self.assertEqual(result['stock_prices'], {'AAPL': 213.26, 'GOOGL': 165.26})
        self.assertEqual(result['cards'], [{'last_digits': '1234', 'total_spent': 300.0, 'cashback': 3.0}])

if __name__ == '__main__':
    unittest.main()