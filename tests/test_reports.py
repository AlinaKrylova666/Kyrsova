import unittest
import pandas as pd
from datetime import datetime
from src.reports import category_expenses_report


def test_category_expenses_report_correct_category(self):
    # Тестируем фильтрацию транзакций по категории 'Еда'
    report = category_expenses_report(self.transactions_df, 'Еда')
    self.assertEqual(len(report), 2)  # Ожидаем 2 транзакции по категории 'Еда'
    self.assertTrue((report['Категория'] == 'Еда').all())

def test_category_expenses_report_date_range(self):
    # Тестируем правильность фильтрации по дате
    specific_date = datetime(2023, 11, 1)
    report = category_expenses_report(self.transactions_df, 'Еда', specific_date)
    self.assertEqual(len(report), 2)  # Ожидаем 2 транзакции за последние три месяца
    self.assertTrue((report['Дата операции'] >= specific_date - pd.DateOffset(months=3)).all())
    self.assertTrue((report['Дата операции'] <= specific_date).all())

def test_category_expenses_report_no_transactions(self):
    # Тестируем случай, когда транзакций по категории нет
    report = category_expenses_report(self.transactions_df, 'Транспорт')
    self.assertEqual(len(report), 0)

if __name__ == '__main__':
    unittest.main()