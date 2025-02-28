import pytest
import json
from src.services import analyze_cashback_categories, find_transactions_with_phone_numbers

def test_analyze_cashback_categories():
    sample_data = [
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 10000, 'description': 'Кафе +7 921 11-22-33'},
        {'year': 2023, 'month': 11, 'category': 'Транспорт', 'amount': 5000, 'description': 'Такси'},
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 7000, 'description': 'Ресторан +7 995 555-55-55'},
    ]

    expected_result = {
        "Еда": 170.0,  # 1% от (10000 + 7000)
        "Транспорт": 50.0  # 1% от 5000
    }

    # Выполнение функции
    result = analyze_cashback_categories(sample_data, 2023, 11)

    # Преобразуем результат обратно в словарь для проверки
    result_dict = json.loads(result)

    assert result_dict == expected_result

def test_find_transactions_with_phone_numbers():
    sample_data = [
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 10000, 'description': 'Кафе +7 921 11-22-33'},
        {'year': 2023, 'month': 11, 'category': 'Транспорт', 'amount': 5000, 'description': 'Такси'},
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 7000, 'description': 'Ресторан +7 995 555-55-55'},
    ]

    expected_result = [
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 10000, 'description': 'Кафе +7 921 11-22-33'},
        {'year': 2023, 'month': 11, 'category': 'Еда', 'amount': 7000, 'description': 'Ресторан +7 995 555-55-55'}
    ]

    # Выполнение функции
    result = find_transactions_with_phone_numbers(sample_data)

    # Преобразуем результат обратно в список для проверки
    result_list = json.loads(result)

    assert result_list == expected_result

# Запуск тестов через командную строку
if __name__ == "__main__":
    pytest.main()
