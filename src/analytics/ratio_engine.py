import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

pl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)

df = pd.merge(
    pl,
    bs,
    on=["company_id", "year"],
    how="inner"
)

# Profit Margin
df["profit_margin_pct"] = (
    df["net_profit"] / df["sales"] * 100
)

# ROE
df["roe_calc_pct"] = (
    df["net_profit"] / df["reserves"] * 100
)

# Debt Ratio
df["debt_ratio_pct"] = (
    df["borrowings"] / df["total_assets"] * 100
)

ratios = df[
    [
        "company_id",
        "year",
        "profit_margin_pct",
        "roe_calc_pct",
        "debt_ratio_pct"
    ]
]

ratios.to_sql(
    "financial_ratio_engine",
    conn,
    if_exists="replace",
    index=False
)

print(ratios.head())

conn.close()