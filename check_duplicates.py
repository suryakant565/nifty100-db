import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

for table in ["profitandloss", "balancesheet", "cashflow"]:

    print(f"\n===== {table} =====")

    df = pd.read_sql(
        f"""
        SELECT company_id,
               year,
               COUNT(*) AS cnt
        FROM {table}
        GROUP BY company_id, year
        HAVING cnt > 1
        LIMIT 20
        """,
        conn
    )

    print(df)

conn.close()