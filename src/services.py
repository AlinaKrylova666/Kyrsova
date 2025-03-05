import pandas as pd
from datetime import datetime


def analyze_cashback_categories(data, year, month):
    filtered_data = filter(
        lambda transaction: pd.to_datetime(transaction['Дата операции']).year == year and pd.to_datetime
        (transaction['Дата операции']).month == month,
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


def category_expenses_report(transactions_df, category, date=None):
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)

    three_months_ago = date - pd.DateOffset(months=3)

    filtered_transactions = transactions_df[
        (transactions_df['Категория'] == category) &
        (transactions_df['Дата операции'] >= three_months_ago) &
        (transactions_df['Дата операции'] <= date)
        ]

    total_expenses = filtered_transactions['Сумма операции с округлением'].sum()

    report = {
        "Категория": category,
        "total_expenses": float(total_expenses),
        "from_date": three_months_ago.strftime('%Y-%m-%d'),
        "to_date": date.strftime('%Y-%m-%d')
    }

    return report

