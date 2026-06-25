import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/nifty100.db")

# Load market_cap table
market_cap = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

# Group by company
summary = (
    market_cap
    .groupby("company_id")
    .agg(
        avg_market_cap=("market_cap_crore", "mean"),
        max_market_cap=("market_cap_crore", "max"),
        min_market_cap=("market_cap_crore", "min"),
        avg_pe_ratio=("pe_ratio", "mean"),
        avg_pb_ratio=("pb_ratio", "mean"),
        avg_dividend_yield=("dividend_yield_pct", "mean")
    )
    .reset_index()
)

# Round numeric columns
numeric_cols = summary.columns.drop("company_id")
summary[numeric_cols] = summary[numeric_cols].round(2)

# Save results to SQLite
summary.to_sql(
    "market_cap_summary",
    conn,
    if_exists="replace",
    index=False
)

print(summary.head())

conn.close()

print("\nMarket Cap Analytics completed successfully!")