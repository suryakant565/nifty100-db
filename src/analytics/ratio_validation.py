import sqlite3
import pandas as pd
import logging
from pathlib import Path

DB_PATH = "data/nifty100.db"

# ---------------------------------------
# Create reports folder
# ---------------------------------------
Path("reports").mkdir(exist_ok=True)

# ---------------------------------------
# Logging Configuration
# ---------------------------------------
logging.basicConfig(
    filename="reports/ratio_edge_cases.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filemode="w"
)

# ---------------------------------------
# Connect Database
# ---------------------------------------
conn = sqlite3.connect(DB_PATH)

# financial_ratios already contains broad_sector
ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

# Source OPM values
profit = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        opm_percentage
    FROM profitandloss
    """,
    conn
)

profit = profit.drop_duplicates(
    subset=["company_id", "year"]
)

# Merge ONLY profit table
merged = ratios.merge(
    profit,
    on=["company_id", "year"],
    how="left"
)

print("=" * 60)
print("Running Ratio Validation")
print("=" * 60)

opm_errors = 0
financial_skipped = 0
roe_skipped = 0
roa_skipped = 0

for _, row in merged.iterrows():

    company = row["company_id"]
    year = row["year"]

    sector = ""

    if pd.notna(row["broad_sector"]):
        sector = str(row["broad_sector"]).strip().lower()

    # ---------------------------------------
    # Skip Financial companies
    # ---------------------------------------
    if sector == "financials":

        logging.info(
            f"Skipped OPM Validation | "
            f"{company} | "
            f"{year} | "
            f"Reason=Financial Sector"
        )

        financial_skipped += 1
        continue

    # ---------------------------------------
    # OPM Validation
    # ---------------------------------------
    if pd.notna(row["opm_percentage"]):

        diff = abs(
            row["operating_profit_margin_pct"]
            - row["opm_percentage"]
        )

        if diff > 1:

            logging.warning(
                f"OPM mismatch | "
                f"{company} | "
                f"{year} | "
                f"Calculated={row['operating_profit_margin_pct']:.2f} | "
                f"Source={row['opm_percentage']:.2f}"
            )

            opm_errors += 1

    # ---------------------------------------
    # ROE skipped
    # ---------------------------------------
    if pd.isna(row["roe_calc_pct"]):

        logging.info(
            f"ROE skipped | "
            f"{company} | "
            f"{year} | "
            f"Reason=Negative Equity"
        )

        roe_skipped += 1

    # ---------------------------------------
    # ROA skipped
    # ---------------------------------------
    if pd.isna(row["roa_pct"]):

        logging.info(
            f"ROA skipped | "
            f"{company} | "
            f"{year} | "
            f"Reason=Zero Assets"
        )

        roa_skipped += 1

logging.info("=" * 60)
logging.info("Validation Completed")
logging.info("=" * 60)

conn.close()

print("\nValidation Summary")
print("-" * 40)
print(f"Financial Companies Skipped : {financial_skipped}")
print(f"OPM Mismatches              : {opm_errors}")
print(f"ROE Skipped                 : {roe_skipped}")
print(f"ROA Skipped                 : {roa_skipped}")

print("\nratio_edge_cases.log generated successfully!")