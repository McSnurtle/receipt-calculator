"""Parse datetime objects to strings and vice-versa

Returns:
    None: N/A
"""
#src/utils/parser.py
# imports
from datetime import datetime

# vars
_format: str = "%Y-%m-%d_%H:%M:%S"

def date_to_str(date: datetime) -> str:
    """Converts a datetime oject to string format %Y-%m-%d_%H:%M:%S

    Args:
        date (datetime): the object to convert

    Returns:
        str: the converted object
    """
    return date.strftime(_format)


def str_to_date(date: str) -> datetime:
    """Converts string of format %Y-%m-%d_%H:%M:%S to a datetime object.

    Args:
        date (str): the string to convert

    Returns:
        datetime: the converted string
    """
    return datetime.strptime(date, _format)


def create_date(year: str, month: str, day: int, hour: int, minute: int,
                second: int = 0) -> datetime:
    """Create a datetime object from args

    Args:
        year (str): 4-digit year
        month (str): 2-digit month
        day (int): day
        hour (int): 24-hour hour
        minute (int): minute
        second (int, optional): second. Defaults to 0.

    Returns:
        datetime: the created object
    """
    return str_to_date(f"{year}-{month}-{day}_{hour}:{minute}:{second}")
