import json
import pandas as pd
import logging
from datetime import datetime, timedelta
from functools import wraps

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Декоратор для записи отчета в файл
def save_report_to_file(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_filename = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_filename, 'w', encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            logging.info(f"Отчет сохранен в файл: {output_filename}")
            return result
        return wrapper
    return decorator

# Функция для получения трат по категории за последние три месяца
@save_report_to_file()
def category_expenses_report(transactions_df, category, date=None):
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    three_months_ago = date - pd.DateOffset(months=3)


    transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'], errors='coerce', dayfirst=True)

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions_df[
        (transactions_df['Категория'] == category) &
        (transactions_df['Дата операции'] >= three_months_ago) &
        (transactions_df['Дата операции'] <= date)
    ]

    # Вычисляем общую сумму трат по категории
    total_expenses = filtered_transactions['Сумма операции с округлением'].sum()

    # Формируем отчет
    report = {
        "Категория": category,
        "total_expenses": float(total_expenses),
        "from_date": three_months_ago.strftime('%Y-%m-%d'),
        "to_date": date.strftime('%Y-%m-%d')
    }

    return report

# Пример использования
if __name__ == "__main__":
    # Пример данных
    data = {
        'Дата операции': ['2023-08-01', '2023-09-15', '2023-10-05', '2023-11-01'],
        'Категория': ['Еда', 'Еда', 'Транспорт', 'Еда'],
        'Сумма операции с округлением': [100, 150, 200, 250]
    }
    transactions_df = pd.DataFrame(data)
    transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'])

    # Генерация отчета
    report = category_expenses_report(transactions_df, 'Еда')
    print(report)
