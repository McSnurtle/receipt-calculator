"""Calculate various different totals based on Receipt objects.

Raises:
    ValueError: when there are 0 people to calculate with.
    ValueError: when there are 0 people to calculate with.

Returns:
    None: N/A
"""
#src/utils/calculator.py
# imports
from typing import Dict
from .models import Receipt, Item  # type: ignore


def average(receipt: Receipt) -> float:
    """Calculates the average amount of money owed per person on the receipt.

    Args:
        receipt (Receipt): The receipt object to calculate.

    Returns:
        float: the average amount of money owed per person on the receipt excluding taxes or tips.
    """

    if not len(receipt.people) > 0:
        raise ValueError("Cannot calculate average with no people!")
    return sum(item.cost for item in receipt.items if isinstance(item, Item)) / len(receipt.people)


def total(receipt: Receipt) -> float:
    """Calculates the total amount of money owed on the receipt.

    Args:
        receipt (Receipt): The receipt object to calculate.

    Returns:
        float: the total amount of money owed on the receipt excluding taxes or tips.
    """

    return sum(item.cost for item in receipt.items if isinstance(item, Item))


def total_with_tax(receipt: Receipt) -> float:
    """Calculates the total amount of money owed on the receipt including tax + tip.

    Args:
        receipt (Receipt): The receipt object to calculate.

    Returns:
        float: the total amount of money owed on the receipt including tax + tip.
    """

    return sum(item.cost * (1 + item.tax + item.tip if item.should_tax else 1 + item.tip) for item
               in receipt.items if isinstance(item, Item))


def total_per_person(receipt: Receipt) -> Dict[str, float]:
    """Calculates the total amount of money owed per person on the receipt based on what they
    purchased.

    Args:
        receipt (Receipt): The receipt object to calculate.

    Returns:
        Dict[str, float]: A dictionary of each user and how much they owe as the values.
    """

    if not len(receipt.people) > 0:
        raise ValueError("Cannot calculate average with no people!")
    debts: Dict[str, float] = {person: 0.0 for person in receipt.people}
    for item in receipt.items:
        if isinstance(item, Item):
            for user in item.users:
                debts[user] += (item.cost * (1 + item.tax + item.tip if item.should_tax else
                                             1 + item.tip)) / len(item.users)
    return debts


def total_per_person_demo(receipt: Receipt) -> Dict[str, float]:
    """Calculates the total amount of money owed per person on the receipt based on what they
    purchased.

    Args:
        receipt (Receipt): The receipt object containing the user / purchase data to calculate

    Returns:
        Dict[str, float]: A dictionary of each user and how much they owe as the values.
    """

    debts: Dict[str, float] = {}    # An empty tracker of debts that will look something like:
    # {
    #   "Jerry": 15.47,
    #   "George": 19.55,
    #   "Elaine": 59.99,
    #   "Kraimer": 4566.99
    # }

    for person in receipt.people:
        debts[person] = 0.0     # Set the base value for all users of items on the receipt

    for item in receipt.items:
        # Add the cost of the item + it's tax and tip percentages to the running total of the
        # end user of the item
        for user in item.users:
            debts[user] += (item.cost * (1 + item.tax + item.tip)) / len(item.users)
    return debts
