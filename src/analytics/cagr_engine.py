import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

pl = pd.read_sql(
    """
    SELECT company_id, year, sales, net_profit
    FROM profitandloss
    """,
    conn
)

results = []

for company in pl["company_id"].unique():

    df = pl[pl["company_id"] == company].copy()

    df = df.sort_values("year")

    if len(df) >= 2:

        start_sales = df.iloc[0]["sales"]
        end_sales = df.iloc[-1]["sales"]

        years = len(df) - 1

        if start_sales > 0:

            sales_cagr = (
                ((end_sales / start_sales) ** (1 / years)) - 1
            ) * 100

            results.append(
                [company, round(sales_cagr, 2)]
            )

cagr_df = pd.DataFrame(
    results,
    columns=[
        "company_id",
        "sales_cagr_pct"
    ]
)

cagr_df.to_sql(
    "cagr_engine",
    conn,
    if_exists="replace",
    index=False
)

print(cagr_df.head())

conn.close()