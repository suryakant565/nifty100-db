import sqlite3
import pandas as pd
import numpy as np

DB_PATH = "data/nifty100.db"


def calculate_cagr(start_value, end_value, periods):
    """
    Safely calculate CAGR.
    """
    if periods <= 0 or start_value <= 0 or end_value <= 0:
        return np.nan

    return ((end_value / start_value) ** (1 / periods) - 1) * 100


conn = sqlite3.connect(DB_PATH)

# Load required tables
pl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)

# Load sector information
sectors = pd.read_sql(
    "SELECT company_id, broad_sector FROM sectors",
    conn
)

# Remove duplicate company-year records
pl = pl.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

bs = bs.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

cf = cf.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

# Merge tables
df = (
    pl.merge(bs, on=["company_id", "year"], how="inner")
      .merge(cf, on=["company_id", "year"], how="left")
      .merge(sectors, on="company_id", how="left")
)
# ----------------------------------
# KPI 1 : Net Profit Margin
# ----------------------------------
df["net_profit_margin_pct"] = np.where(
    df["sales"] == 0,
    np.nan,
    (df["net_profit"] / df["sales"]) * 100
)

# ----------------------------------
# KPI 2 : Operating Profit Margin
# ----------------------------------
df["operating_profit_margin_pct"] = np.where(
    df["sales"] == 0,
    np.nan,
    (df["operating_profit"] / df["sales"]) * 100
)

# ----------------------------------
# OPM Source Validation
# ----------------------------------

df["opm_difference"] = (
    df["operating_profit_margin_pct"] -
    df["opm_percentage"]
).abs()

df["opm_validation"] = np.where(
    df["opm_difference"] > 1,
    "FAIL",
    "PASS"
)

# ----------------------------------
# KPI 3 : ROE
# ----------------------------------
equity_base = df["equity_capital"] + df["reserves"]

df["roe_calc_pct"] = np.where(
    equity_base <= 0,
    np.nan,
    (df["net_profit"] / equity_base) * 100
)

# ----------------------------------
# KPI 4 : ROCE
# ----------------------------------
ebit = df["operating_profit"] + df["other_income"]

capital_employed = (
    df["equity_capital"]
    + df["reserves"]
    + df["borrowings"]
)

df["roce_calc_pct"] = np.where(
    capital_employed <= 0,
    np.nan,
    (ebit / capital_employed) * 100
)

# ----------------------------------
# ROCE Benchmark Type
# ----------------------------------

df["roce_benchmark"] = np.where(
    df["broad_sector"].fillna("").str.lower() == "financials",
    "Sector Relative",
    "Absolute"
)
# ----------------------------------
# KPI 5 : Debt to Equity
# ----------------------------------

df["debt_to_equity"] = np.where(
    df["borrowings"] == 0,
    0,
    np.where(
        equity_base <= 0,
        np.nan,
        df["borrowings"] / equity_base
    )
)

# ----------------------------------
# High Leverage Flag
# ----------------------------------

df["high_leverage_flag"] = (
    (df["debt_to_equity"] > 5) &
    (df["broad_sector"].fillna("").str.lower() != "financials")
)

# ----------------------------------
# KPI 6 : Return on Assets (ROA)
# ----------------------------------
df["roa_pct"] = np.where(
    df["total_assets"] == 0,
    np.nan,
    (df["net_profit"] / df["total_assets"]) * 100
)

# ----------------------------------
# KPI 7 : Interest Coverage
# ----------------------------------

df["interest_coverage"] = np.where(
    df["interest"] == 0,
    np.nan,
    (df["operating_profit"] + df["other_income"]) / df["interest"]
)

# ----------------------------------
# ICR Label
# ----------------------------------

df["icr_label"] = np.where(
    df["interest"] == 0,
    "Debt Free",
    None
)

# ----------------------------------
# ICR Warning Flag
# ----------------------------------

df["icr_warning_flag"] = np.where(
    df["interest_coverage"] < 1.5,
    True,
    False
)

# ----------------------------------
# KPI 8 : Net Debt
# ----------------------------------

df["net_debt"] = (
    df["borrowings"] -
    df["investments"]
)

# ----------------------------------
# KPI 8 : Asset Turnover
# ----------------------------------
df["asset_turnover"] = np.where(
    df["total_assets"] == 0,
    np.nan,
    df["sales"] / df["total_assets"]
)

# ----------------------------------
# KPI 9 : Free Cash Flow
# ----------------------------------
df["free_cash_flow"] = (
    df["operating_activity"]
    + df["investing_activity"]
)

# ----------------------------------
# KPI 10 : Revenue CAGR
# ----------------------------------
df["revenue_cagr_pct"] = np.nan

for company in df["company_id"].unique():

    company_rows = (
        df[df["company_id"] == company]
        .sort_values("year")
    )

    if len(company_rows) >= 2:

        start_sales = company_rows.iloc[0]["sales"]
        end_sales = company_rows.iloc[-1]["sales"]

        periods = len(company_rows) - 1

        cagr = calculate_cagr(
            start_sales,
            end_sales,
            periods
        )

        df.loc[
            df["company_id"] == company,
            "revenue_cagr_pct"
        ] = round(cagr, 2)

# Round KPI columns
kpi_cols = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "roe_calc_pct",
    "roce_calc_pct",
    "roa_pct",
    "debt_to_equity",
    "high_leverage_flag",
    "interest_coverage",
    "net_debt",
    "asset_turnover",
    "free_cash_flow",
    "revenue_cagr_pct"
]

df[kpi_cols] = df[kpi_cols].round(2)

# Save required output table
output = df[
    [
        "company_id",
        "year",
        "broad_sector",
        *kpi_cols,
        "icr_label",
        "icr_warning_flag",
        "opm_difference",
        "opm_validation",
        "roce_benchmark"
    ]
]

output.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print(output.head())
print(f"\nRows written: {len(output)}")

conn.close()

print("\nfinancial_ratios table created successfully!")