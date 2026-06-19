import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"

raw_files = {
    "companies": "data/raw/companies.xlsx",
    "profitandloss": "data/raw/profitandloss.xlsx",
    "balancesheet": "data/raw/balancesheet.xlsx",
    "cashflow": "data/raw/cashflow.xlsx",
    "analysis": "data/raw/analysis.xlsx",
    "documents": "data/raw/documents.xlsx",
    "prosandcons": "data/raw/prosandcons.xlsx",
}

supporting_files = {
    "sectors": "data/supporting/sectors.xlsx",
    "stock_prices": "data/supporting/stock_prices.xlsx",
    "market_cap": "data/supporting/market_cap.xlsx",
    "financial_ratios": "data/supporting/financial_ratios.xlsx",
    "peer_groups": "data/supporting/peer_groups.xlsx"
}

conn = sqlite3.connect(DB_PATH)

# Core files need header=1
for table, file in raw_files.items():
    df = pd.read_excel(file, header=1)
    df.to_sql(table, conn, if_exists="replace", index=False)
    print(f"{table}: {len(df)} rows loaded")

# Supporting files use normal header
for table, file in supporting_files.items():
    df = pd.read_excel(file)
    df.to_sql(table, conn, if_exists="replace", index=False)
    print(f"{table}: {len(df)} rows loaded")

conn.close()

print("\nAll datasets loaded successfully!")