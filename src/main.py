from src.views import generate_main_page
from src.services import analyze_cashback_categories
from src.reports import category_expenses_report
import pandas as pd
import os

def main():
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.join(current_dir, "..")
    operations_path = os.path.join(root_dir, "data", "operations.xlsx")
    transactions_df = pd.read_excel(operations_path)

    transactions_as_dicts = transactions_df.to_dict(orient='records')

    main_page_info = generate_main_page(transactions_df, '2021-12-11 01:02:03')
    print(main_page_info)

    service_info = analyze_cashback_categories(transactions_as_dicts, 2021, 11)
    print(service_info)

    report_info = category_expenses_report(transactions_df, 'Еда')
    print(report_info)


if __name__ == "__main__":
    main()