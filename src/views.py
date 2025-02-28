import json
import requests
from datetime import datetime
import pandas as pd


# Загрузка пользовательских настроек
def load_user_settings():
    with open('user_settings.json', 'r') as file:
        settings = json.load(file)
    return settings


# Функция для получения приветствия в зависимости от времени
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


# Функция для получения курса валют
def get_currency_rates(currencies):
    # Здесь необходимо использовать API для получения курсов валют
    # Пример: запрос к какому-либо сервису
    rates = {}
    for currency in currencies:
        # Пример запроса к фиктивному API
        response = requests.get(f"https://api.example.com/currency?symbol={currency}")
        data = response.json()
        rates[currency] = data['rate']
    return rates


# Функция для получения цен на акции
def get_stock_prices(stocks):
    # Здесь необходимо использовать API для получения цен на акции
    prices = {}
    for stock in stocks:
        # Пример запроса к фиктивному API
        response = requests.get(f"https://api.example.com/stocks?symbol={stock}")
        data = response.json()
        prices[stock] = data['price']
    return prices


# Главная функция
def generate_report(date_time_str):
    settings = load_user_settings()

    # Преобразование строки даты и времени в объект datetime
    current_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Приветствие
    greeting = get_greeting(current_time)

    # Курсы валют
    currency_rates = get_currency_rates(settings['user_currencies'])

    # Цены на акции
    stock_prices = get_stock_prices(settings['user_stocks'])

    # Формирование JSON-ответа
    response = {
        "greeting": greeting,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
        # Добавьте сюда данные по картам и транзакциям
    }

    return json.dumps(response, ensure_ascii=False)


# Пример использования
if __name__ == "__main__":
    print(generate_report("2023-11-01 14:30:00"))
