import re
from datetime import datetime
from typing import Optional

from utils import consts


def extract_float_from_text(text: str) -> Optional[float]:
    match = re.search(r'\d+\.\d+', text)
    if match:
        return float(match.group())
    return None


def extract_price_from_text(text: str) -> Optional[int]:
    match = re.search(r'₪\s*(\d+(?:\.\d+)?)', text)
    if match:
        return round(float(match.group(1)))
    return None


def remove_float(text: str):
    return re.sub(r'\.(\d+)', '', text)


def remove_nonbreaking_spaces(text: str):
    return text.replace("\xa0", " ")


def format_date(text: str):
    return datetime.strptime(text, consts.DATE_FORMAT)


# parse dates like "May 26–27" to datetime
def parse_checkin_checkout(date_str: str):
    clean_str = date_str.replace('\u2009', '').replace('–', '-').replace('\u2013', '-').strip()

    month_and_day_from, day_to_str = clean_str.split('-')
    month_str, day_from_str = month_and_day_from.split()
    day_from = int(day_from_str)
    day_to = int(day_to_str)
    year = datetime.now().year
    month = datetime.strptime(month_str, '%b').month

    check_in = datetime(year, month, day_from)
    check_out = datetime(year, month, day_to)

    return check_in, check_out
