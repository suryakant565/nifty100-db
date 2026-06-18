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

    # Handles: Mar 2014, Dec 2012, Jun 2015
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

    except:
        pass

    if year.upper() == "TTM":
        return "TTM"

    return "PARSE_ERROR"