import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/nifty100.db")

# Load required tables
peer_groups = pd.read_sql("SELECT * FROM peer_groups", conn)
market_cap = pd.read_sql("SELECT * FROM market_cap_summary", conn)

# Merge peer groups with market cap summary
peer_summary = pd.merge(
    peer_groups,
    market_cap,
    on="company_id",
    how="left"
)

# Calculate peer group averages
peer_analysis = (
    peer_summary
    .groupby("peer_group_name")
    .agg(
        companies=("company_id", "count"),
        avg_market_cap=("avg_market_cap", "mean"),
        avg_pe_ratio=("avg_pe_ratio", "mean"),
        avg_pb_ratio=("avg_pb_ratio", "mean"),
        avg_dividend_yield=("avg_dividend_yield", "mean")
    )
    .reset_index()
)

# Round numeric columns
numeric_cols = peer_analysis.columns.drop(["peer_group_name"])
peer_analysis[numeric_cols] = peer_analysis[numeric_cols].round(2)

# Save to SQLite
peer_analysis.to_sql(
    "peer_group_summary",
    conn,
    if_exists="replace",
    index=False
)

print(peer_analysis.head())

conn.close()

print("\nPeer Comparison completed successfully!")