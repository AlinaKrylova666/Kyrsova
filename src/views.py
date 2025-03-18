from datetime import datetime
from src.utils import load_user_settings, get_greeting, get_currency_rates, get_stock_prices, collect_cards_data, get_top_transactions
import pandas as pd

def generate_main_page(transactions_df, date_time_str):
    settings = load_user_settings()
    end_period = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    start_period = end_period.replace(day=1, hour=0, minute=0, second=0)

    # Фильтруем транзакции по заданному периоду
    only_in_period = transactions_df.loc[
        (pd.to_datetime(transactions_df["Дата операции"], dayfirst=True) >= start_period) &
        (pd.to_datetime(transactions_df["Дата операции"], dayfirst=True) <= end_period)
    ]

    # Фильтруем только расходы
    expenses_only = only_in_period.loc[only_in_period["Сумма операции"] < 0]

    current_time = datetime.now()
    greeting = get_greeting(current_time)
    cards_info = collect_cards_data(expenses_only)
    top_five = get_top_transactions(only_in_period)

    currency_rates = get_currency_rates(settings['user_currencies'])
    stock_prices = get_stock_prices(settings['user_stocks'])

    # Формируем ответ в виде словаря
    response = {
        "greeting": greeting,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
        "cards": cards_info,
        "top_transactions": top_five  # Добавляем топ транзакции в ответ
    }
    return response

# Пример использования
if __name__ == "__main__":
    df = pd.read_excel('../data/operations.xlsx')
    result = generate_main_page(df, '2021-11-30 05:05:05')
    print(result)
