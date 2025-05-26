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


def parse_checkin_checkout(date_str: str):
    try:
        date_str = date_str.replace('\u2009', '').replace('\u2013', '-').replace('–', '-').strip()

        parts = date_str.split(' ', 1)
        if len(parts) != 2:
            raise ValueError(f"Unexpected format: {date_str}")

        month_str, day_range = parts
        day_from, day_to = map(int, day_range.split('-'))

        current_year = datetime.now().year
        month_number = datetime.strptime(month_str, '%b' if len(month_str) == 3 else '%B').month

        check_in = datetime.strptime(f"{day_from}/{month_number}/{current_year}", "%d/%m/%Y")
        check_out = datetime.strptime(f"{day_to}/{month_number}/{current_year}", "%d/%m/%Y")

        return check_in, check_out
    except Exception as e:
        raise ValueError(f"Invalid date format '{date_str}': {e}")
