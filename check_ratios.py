import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratio_engine
    LIMIT 10
    """,
    conn
)

print(df)

conn.close()