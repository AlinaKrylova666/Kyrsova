import unittest
import pandas as pd
from datetime import datetime
from src.services import analyze_cashback_categories

class TestAnalyzeCashbackCategories(unittest.TestCase):
    def setUp(self):
        # Пример данных для тестов
        self.data = [
            {'Дата операции': '01.08.2023', 'Категория': 'Еда', 'Сумма операции с округлением': 100},
            {'Дата операции': '15.08.2023', 'Категория': 'Транспорт', 'Сумма операции с округлением': 200},
            {'Дата операции': '05.09.2023', 'Категория': 'Еда', 'Сумма операции с округлением': 150},
            {'Дата операции': '01.09.2023', 'Категория': 'Развлечения', 'Сумма операции с округлением': 50},
        ]

    def test_cashback_calculation_for_august_2023(self):
        # Тестирование для августа 2023 года
        result = analyze_cashback_categories(self.data, 2023, 8)
        expected = {
            'Еда': 1.0,  # 100 * 0.01
            'Транспорт': 2.0  # 200 * 0.01
        }
        self.assertEqual(result, expected)

    def test_cashback_calculation_for_september_2023(self):
        # Тестирование для сентября 2023 года
        result = analyze_cashback_categories(self.data, 2023, 9)
        expected = {
            'Еда': 1.5,  # 150 * 0.01
            'Развлечения': 0.5  # 50 * 0.01
        }
        self.assertEqual(result, expected)

    def test_no_transactions_for_month(self):
        # Тестирование для месяца без транзакций
        result = analyze_cashback_categories(self.data, 2023, 10)
        expected = {}
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
