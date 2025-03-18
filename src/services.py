import pandas as pd
from datetime import datetime


def analyze_cashback_categories(data, year, month):
    filtered_data = filter(
        lambda transaction: pd.to_datetime(transaction['Дата операции'], dayfirst=True).year == year and pd.to_datetime
        (transaction['Дата операции'], dayfirst=True).month == month,
        data
    )

    cashback_summary = {}
    for transaction in filtered_data:
        category = transaction['Категория']
        amount = transaction['Сумма операции с округлением']
        cashback = amount * 0.01

        if category in cashback_summary:
            cashback_summary[category] += cashback
        else:
            cashback_summary[category] = cashback

    return cashback_summary
