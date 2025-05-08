#src/utils/parser.py
# imports
from datetime import datetime

# vars
format: str = "%Y-%m-%d_%H:%M:%S"

def date_to_str(date: datetime) -> str:
    return date.strftime(format)


def str_to_date(date: str) -> datetime:
    return datetime.strptime(date, format)


def create_date(year: str, month: str, day: int, hour: int, minute: int, second: int = 0) -> datetime:
    return date_to_str(f"{year}-{month}-{day}_{hour}:{minute}:{second}")
