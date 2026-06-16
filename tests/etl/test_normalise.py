from src.etl.normaliser import normalize_ticker, normalize_year


print(normalize_ticker(" tcs "))
print(normalize_ticker("m&m"))
print(normalize_ticker("bajaj-auto"))

print(normalize_year("Mar-23"))
print(normalize_year("FY24"))
print(normalize_year("Dec-22"))
print(normalize_year("2023"))
print(normalize_year("xyz"))