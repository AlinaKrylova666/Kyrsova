import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Загрузите переменные окружения из файла .env
load_dotenv()

# Получите ключи API из переменных окружения
CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')
STOCK_API_KEY = os.getenv('STOCK_API_KEY')

def load_user_settings():
    with open('C:/Users/user/PycharmProjects/PythonProject5/user_settings.json', 'r') as file:
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
    url = f"https://api.exchangerate-api.com/v4/latest/USD?apikey={CURRENCY_API_KEY}"
    response = requests.get(url)
    data = response.json()
    rates = {currency: data['rates'].get(currency, None) for currency in currencies}
    return rates

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

def generate_report(transactions_df, date_time_str):
    settings = load_user_settings()
    current_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    greeting = get_greeting(current_time)

    currency_rates = get_currency_rates(settings['user_currencies'])
    stock_prices = get_stock_prices(settings['user_stocks'])

    response = {
        "greeting": greeting,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return response
