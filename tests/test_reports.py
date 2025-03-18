import unittest
import pandas as pd
from datetime import datetime
from src.reports import category_expenses_report

class TestCategoryExpensesReport(unittest.TestCase):

    def setUp(self):
        # Подготавливаем данные для тестов
        self.transactions_df = pd.DataFrame({
            'Дата операции': ['2023-08-01', '2023-09-15', '2023-10-05', '2023-11-01'],
            'Категория': ['Еда', 'Еда', 'Транспорт', 'Еда'],
            'Сумма операции': [-100, -150, 200, -250]  # Отрицательные значения для расходов
        })
        self.transactions_df['Дата операции'] = pd.to_datetime(self.transactions_df['Дата операции'])

    def test_no_negative_expenses_for_category(self):
        # Ожидаем 0 транзакций по категории 'Еда' с отрицательной суммой, так как все положительные
        report = category_expenses_report(self.transactions_df, 'Еда')
        self.assertEqual(len(report), 0, "Ожидаем 0 транзакций по категории 'Еда' с отрицательной суммой")

    def test_expenses_within_date_range(self):
        # Ожидаем 3 транзакции за последние три месяца по категории 'Еда', независимо от суммы
        specific_date = datetime(2023, 11, 1)
        report = category_expenses_report(self.transactions_df, 'Еда', specific_date)
        self.assertEqual(len(report), 3, "Ожидаем 3 транзакции за последние три месяца")
        self.assertTrue((report['Дата операции'] >= specific_date - pd.DateOffset(months=3)).all(),
                        "Все даты операций должны быть в пределах трех месяцев от указанной даты")
        self.assertTrue((report['Дата операции'] <= specific_date).all(),
                        "Все операции должны быть до указанной даты")

    def test_no_transactions_for_nonexistent_category(self):
        # Ожидаем 0 транзакций для несуществующей категории
        report = category_expenses_report(self.transactions_df, 'Не существует')
        self.assertEqual(len(report), 0, "Ожидаем 0 транзакций для несуществующей категории")

if __name__ == '__main__':
    unittest.main()

