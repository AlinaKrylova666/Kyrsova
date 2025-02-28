import pytest
import pandas as pd
from src.reports import category_expenses_report

# Функция для тестирования отчета по тратам
def test_category_expenses_report():
    data = {
        'date': ['2023-08-01', '2023-09-15', '2023-10-05', '2023-11-01'],
        'category': ['Еда', 'Еда', 'Транспорт', 'Еда'],
        'amount': [100, 150, 200, 250]
    }
    transactions_df = pd.DataFrame(data)
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])

    # Ожидаемый результат
    expected_report = {
        "category": "Еда",
        "total_expenses": 500.0,  # Сумма за последние три месяца (250 + 150 + 100)
        "from_date": (pd.to_datetime('2023-11-01') - pd.Timedelta(days=90)).strftime('%Y-%m-%d'),
        "to_date": '2023-11-01'
    }

    # Генерация отчета
    report = category_expenses_report(transactions_df, 'Еда', '2023-11-01')

    # Проверка, что результат соответствует ожиданиям
    assert report['category'] == expected_report['category']
    assert report['total_expenses'] == expected_report['total_expenses']
    assert report['from_date'] == expected_report['from_date']
    assert report['to_date'] == expected_report['to_date']

# Запуск тестов через командную строку
if __name__ == "__main__":
    pytest.main()
