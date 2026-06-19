import pandas as pd
import sqlite3
from datetime import datetime

db_path = "data/nifty100.db"

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "market_cap",
    "financial_ratios",
    "peer_groups"
]

conn = sqlite3.connect(db_path)

audit = []

for table in tables:
    count = pd.read_sql(
        f"SELECT COUNT(*) as cnt FROM {table}",
        conn
    )["cnt"][0]

    audit.append({
        "table_name": table,
        "rows_out": count,
        "timestamp": datetime.now()
    })

conn.close()

audit_df = pd.DataFrame(audit)

audit_df.to_csv("load_audit.csv", index=False)

print(audit_df)
print("\nload_audit.csv created successfully")