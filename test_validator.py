import pandas as pd

from src.etl.loader import load_excel
from src.etl.validator import validate_dataframe

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
]

all_failures = []

for file in files:

    path = f"data/raw/{file}"

    try:
        df = load_excel(path)

        failures = validate_dataframe(df, file)

        all_failures.extend(failures)

        print(f"{file}: {len(failures)} issues")

    except Exception as e:
        print(file, e)

columns = [
    "file_name",
    "row_number",
    "field",
    "issue",
    "severity",
]

failure_df = pd.DataFrame(all_failures, columns=columns)

failure_df.to_csv(
    "validation_failures.csv",
    index=False
)

print("\nSaved validation_failures.csv")