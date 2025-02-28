import json
import re
from datetime import datetime
from functools import reduce

# Функция для анализа выгодности категорий повышенного кешбэка
def analyze_cashback_categories(data, year, month):
    # Фильтруем транзакции за указанный год и месяц
    filtered_data = filter(
        lambda transaction: transaction['year'] == year and transaction['month'] == month,
        data
    )

    # Вычисляем кешбэк для каждой категории
    cashback_summary = {}
    for transaction in filtered_data:
        category = transaction['category']
        amount = transaction['amount']
        cashback = amount * 0.01  # 1% кешбэк

        if category in cashback_summary:
            cashback_summary[category] += cashback
        else:
            cashback_summary[category] = cashback

    # Преобразуем результат в JSON
    return json.dumps(cashback_summary, ensure_ascii=False)

# Функция для поиска транзакций по телефонным номерам
def find_transactions_with_phone_numbers(data):
    # Регулярное выражение для поиска телефонных номеров
    phone_pattern = re.compile(r'\+7 \d{3} \d{2}-\d{2}-\d{2}')

    # Фильтруем транзакции, содержащие телефонные номера
    transactions_with_phones = filter(
        lambda transaction: phone_pattern.search(transaction['description']),
        data
    )

    # Преобразуем в список и затем в JSON
    transactions_list = list(transactions_with_phones)
    return json.dumps(transactions_list, ensure_ascii=False)

# Пример использования
if __name__ == "__main__":
    sample_data = [
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 10000, 'description': 'Кафе +7 921 11-22-33'},
        {'year': 2023, 'month': 11, 'category': 'Транспорт', 'amount': 5000, 'description': 'Такси'},
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 7000, 'description': 'Ресторан +7 995 555-55-55'},
    ]

    cashback_result = analyze_cashback_categories(sample_data, 2023, 11)
    phone_result = find_transactions_with_phone_numbers(sample_data)

    print("Анализ кешбэка:", cashback_result)
    print("Транзакции с номерами:", phone_result)
