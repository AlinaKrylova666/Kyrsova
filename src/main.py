from src.views import generate_report
from src.services import analyze_cashback_categories, category_expenses_report
import pandas as pd


def main():
    transactions_df = pd.read_excel('C:/Users/user/PycharmProjects/PythonProject5/data/operations.xlsx')

    transactions_as_dicts = transactions_df.to_dict(orient='records')

    main_page_info = generate_report(transactions_df, '2021-12-11 01:02:03')
    print(main_page_info)

    service_info = analyze_cashback_categories(transactions_as_dicts, 2021, 11)
    print(service_info)

    report_info = category_expenses_report(transactions_df, 'Еда')
    print(report_info)


if __name__ == "__main__":
    main()