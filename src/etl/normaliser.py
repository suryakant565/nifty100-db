from datetime import datetime
import re


def normalize_ticker(ticker):
    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_year(year):
    year = str(year).strip()

    if re.match(r"^\d{4}-\d{2}$", year):
        return year

    if re.match(r"^FY\d{2}$", year):
        yy = int(year[-2:])
        return f"20{yy:02d}-03"

    # Handles: Mar 2016 9m, Mar 2023 15
    match = re.match(r"^([A-Za-z]{3})\s+(\d{4})\s+\d+[A-Za-z]*$", year)
    if match:
        month, yr = match.groups()
        try:
            dt = datetime.strptime(f"{month} {yr}", "%b %Y")
            return dt.strftime("%Y-%m")
        except:
            pass

    try:
        dt = datetime.strptime(year, "%b-%y")
        return dt.strftime("%Y-%m")
    except:
        pass

    try:
        dt = datetime.strptime(year, "%b %y")
        return dt.strftime("%Y-%m")
    except:
        pass

    try:
        dt = datetime.strptime(year, "%B-%Y")
        return dt.strftime("%Y-%m")
    except:
        pass

    try:
        dt = datetime.strptime(year, "%b %Y")
        return dt.strftime("%Y-%m")
    except:
        pass

    if year.isdigit() and len(year) == 4:
        return f"{year}-03"

    try:
        value = float(year)

        if value.is_integer():
            return f"{int(value)}-03"

        if 1900 <= int(value) <= 2100:
            return f"{int(value)}-03"

    except:
        pass

    if year.upper() == "TTM":
        return "TTM"

    return "PARSE_ERROR"