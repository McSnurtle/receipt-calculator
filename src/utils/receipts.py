#src/utils/receipts.py
# imports
import os
import json
from typing import List, Dict, Union
from .models import Receipt # type: ignore

# *******************************
# FUNCTIONS
# *******************************

def get_last_receipt() -> int | None:
    """Returns the name of the last receipt that was used according to `etc/conf.json`. If `null`, returns `None`

    Returns:
          int | None: The id of the last receipt used as found in `etc/conf.json` if any.
    """
    with open("etc/conf.json", "r", encoding="utf-8") as f:
        rid: int | None = json.load(f)["lastReceipt"]
        if rid in receipts_by_id.keys():    # if a receipt with that ID exists...
            return rid


def get_receipts() -> List[Union[Receipt, object]]:    # this whole function could be compressed into a single line with list comprehension! I've resisted the temptation in the name of readability :eyes:
    """Returns a list of Receipt-like objects derived from `data/receipts/`"""

    _receipts: List[Union[Receipt, object]] = []
    filepaths: List[str] = [file for file in os.listdir("data/receipts/") if file.endswith(".json")]

    for filename in filepaths:
        with open(f"data/receipts/{filename}", "r", encoding="utf-8") as f:
            receipt: object = Receipt.from_dict(data=json.load(f))
            _receipts.append(receipt)
    return _receipts


def get_receipts_compact() -> List[Union[Receipt, object]]:    # and for the aforementioned compacted version...
    """Returns a list of Receipt-like objects derived from `data/receipts/`"""

    return [receipt for receipt in [Receipt.from_dict(json.load(f) for f in [open(f"data/receipts/{filename}", "r", encoding="utf-8") for filename in [file for file in os.listdir("data/receipts/") if file.endswith(".json")]])]]


def get_receipt_file(filename: str) -> Union[Receipt, object]:
    """Returns a Receipt object based on stored data.

    :param filename: str, the filename of the receipt to check for excluding file types / extensions.

    :return receipt: Receipt, the Receipt like object to return containing item information."""

    filepath: str = f"data/receipts/{filename}.json"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return Receipt.from_dict(json.load(f))
    raise FileNotFoundError(f"Coulnd't find '{filepath}.json' in `data/receipts/`!")


def get_receipt_by_id(rid: int) -> Receipt:
    """Returns a Receipt object based on stored data.

    :param rid: int, the id of the stored receipt to return.

    :return receipt: Receipt, the Receipt like object to return containing item information."""

    return receipts_by_id[rid]


def last_id() -> int:
    """Returns the latest (greatest) id of saved receipts"""
    _receipts: List[Union[Receipt, object]]= get_receipts()
    return max([receipt.id for receipt in receipts if isinstance(receipt, Receipt)])


# ******************************
# VARIABLES
# *******************************

receipts: List[Union[Receipt, object]] = get_receipts()
receipts_by_id: Dict[int, Receipt] = {receipt.id: receipt for receipt in receipts if isinstance(receipt, Receipt)}
