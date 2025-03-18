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
            result:pd.DataFrame = func(*args, **kwargs)
            output_filename = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            result.to_json(path_or_buf=output_filename, indent=4, force_ascii=False, orient="records")
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
        (transactions_df['Дата операции'] <= date) &
        (transactions_df['Сумма операции'] < 0)
    ]
    return filtered_transactions

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
