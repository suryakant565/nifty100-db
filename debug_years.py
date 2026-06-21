from src.etl.loader import load_excel
from src.etl.normaliser import normalize_year

df = load_excel("data/raw/profitandloss.xlsx")

for idx in [96, 485, 986]:
    value = df.loc[idx, "year"]
    print(idx, repr(value), "->", normalize_year(value))