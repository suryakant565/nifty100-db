import pandas as pd

from src.etl.normaliser import normalize_ticker, normalize_year


def validate_dataframe(df, file_name):
    failures = []

    # company_id validation
    if "company_id" in df.columns:

        for idx, value in enumerate(df["company_id"]):

            if pd.isna(value):
                failures.append(
                    [file_name, idx, "company_id",
                     "Missing company_id", "CRITICAL"]
                )

            else:
                ticker = normalize_ticker(value)

                if ticker == "":
                    failures.append(
                        [file_name, idx, "company_id",
                         "Blank company_id", "CRITICAL"]
                    )

    # year validation
    if "year" in df.columns:

        for idx, value in enumerate(df["year"]):

            year = normalize_year(value)

            if year == "PARSE_ERROR":
                failures.append(
                    [file_name, idx, "year",
                     f"Invalid year: {value}", "CRITICAL"]
                )

    # duplicate company-year check
    if {"company_id", "year"}.issubset(df.columns):

        duplicates = df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )

        for idx in df[duplicates].index:

            failures.append(
                [file_name, idx, "(company_id, year)",
                 "Duplicate company-year record",
                 "WARNING"]
            )

    return failures