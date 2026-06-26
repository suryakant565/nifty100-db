import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    LIMIT 10
    """,
    conn
)

print(df)
print("\nColumns:", len(df.columns))
print("Rows:", len(pd.read_sql("SELECT * FROM financial_ratios", conn)))

conn.close()