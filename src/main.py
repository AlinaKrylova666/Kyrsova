from src.reports import category_expenses_report
import pandas as pd

def main():
    # Пример данных
    data = {
        'date': ['2023-08-01', '2023-09-15', '2023-10-05', '2023-11-01'],
        'category': ['Еда', 'Еда', 'Транспорт', 'Еда'],
        'amount': [100, 150, 200, 250]
    }
    transactions_df = pd.DataFrame(data)
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])

    # Генерация отчета
    report = category_expenses_report(transactions_df, 'Еда')
    print("Отчет по тратам:", report)

if __name__ == "__main__":
    main()
