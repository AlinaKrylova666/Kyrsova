import json
import os
import pandas as pd

import requests
from dotenv import load_dotenv

# Загрузите переменные окружения из файла .env
load_dotenv()

# Получите ключи API из переменных окружения
CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')
STOCK_API_KEY = os.getenv('STOCK_API_KEY')

current_dir = os.path.dirname(__file__)
root_dir = os.path.join(current_dir, "..")
user_settings_path = os.path.join(root_dir, "user_settings.json")

def load_user_settings():
    with open(user_settings_path, 'r') as file:
        settings = json.load(file)
    return settings


def get_greeting(current_time):
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies):
    result = []
    for currency in currencies:

        url = f"https://api.exchangerate-api.com/v4/latest/{currency}?apikey={CURRENCY_API_KEY}"
        response = requests.get(url)
        data = response.json()
        result.append({"currency": currency, "rate": data['rates'].get("RUB", None)})
    return result


def get_stock_prices(stocks):
    prices = {}
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey={STOCK_API_KEY}"
        response = requests.get(url)
        data = response.json()
        time_series = data.get("Time Series (1min)", {})
        latest_time = sorted(time_series.keys())[0] if time_series else None
        prices[stock] = float(time_series[latest_time]["1. open"]) if latest_time else None
    return prices

def collect_cards_data(data):
    grouped_bay_card = data.groupby("Номер карты")
    agg_info = grouped_bay_card.agg(total_spent=("Сумма операции", lambda x: round(abs(sum(x)), 2)),
                                    cashback=("Сумма операции", lambda x: round(abs(sum(x))* 0.01, 2)))
    cards_info = []
    for card_number, info in agg_info.iterrows():
        current_card = {}
        current_card["last_digits"] = card_number.strip("*")
        current_card.update(info.to_dict())
        cards_info.append(current_card)
    return cards_info


def get_top_transactions(data: pd.DataFrame):
    # Сортируем данные по сумме операции
    sorted_by_price = data.sort_values("Сумма операции")
    # Выбираем 5 топовых транзакций
    top_five = sorted_by_price.nlargest(5, "Сумма операции")

    # Убедимся, что даты в формате datetime
    top_five['Дата операции'] = pd.to_datetime(top_five['Дата операции'], errors='coerce', dayfirst=True)

    # Формируем список словарей
    result = []
    for index, info in top_five.iterrows():
        current_line_info = {
            'category': info['Категория'],  # Категория
            'amount': info['Сумма операции'],  # Сумма
            'description': info['Описание'],  # Описание
            'date': info['Дата операции'].date() if pd.notnull(info['Дата операции']) else None  # Дата, без времени
        }
        result.append(current_line_info)

    return result

# Пример вызова функции
if __name__ == "__main__":
    # Создаем тестовый DataFrame
    data = pd.DataFrame({
        'Дата операции': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'],
        'Категория': ['Еда', 'Развлечения', 'Транспорт', 'Одежда', 'Электроника'],
        'Сумма операции': [100, 150, 200, 250, 300],
        'Описание': ['Покупка продуктов', 'Кино', 'Проезд', 'Покупка одежды', 'Техника']
    })
    top_transactions = get_top_transactions(data)
    print(top_transactions)
