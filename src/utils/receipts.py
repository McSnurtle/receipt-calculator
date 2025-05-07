#src/utils/receipts.py
# imports
import os
import json
from typing import Any, List, Dict
from .models import Receipt

# *******************************
# FUNCTIONS
# *******************************

def get_last_receipt() -> str | None:
    with open(f"etc/conf.json", "r") as f:
        last_receipt: str | None = json.loads(f)["lastReceipt"]
        if os.path.exists(f"data/receipts/{last_receipt}.json"):
            return last_receipt
    return


def get_receipts() -> List[Receipt]:    # this whole function could be compressed into a single line with list comprehension! I've resisted the temptation in the name of readability :eyes:
    """Returns a list of Receipt-like objects derived from `data/receipts/`"""

    receipts: List[Receipt] = []
    filepaths: List[str] = [file for file in os.listdir(f"data/receipts/") if file.endswith(".json")]

    for filename in filepaths:
        with open(f"data/receipts/{filename}", "r") as f:
            receipt: Receipt = Receipt.from_dict(data=json.load(f))
            receipts.append(receipt)
    return receipts


def get_receipts_compact() -> List[Receipt]:    # and for the aforementioned compacted version...
    """Returns a list of Receipt-like objects derived from `data/receipts/`"""
    
    return [receipt for receipt in [Receipt.to_dict(json.reads(fp) for fp in [open(f"data/receipts/{filename}") for filename in [file for file in os.listdir("data/receipts/") if file.endswith(".json")]])]]
            
        
def get_receipt_file(filename: str) -> Receipt:
    """Returns a Receipt object based on stored data.
    
    :param filename: str, the filename of the receipt to check for excluding file types / extensions.
    
    :return receipt: Receipt, the Receipt like object to return containing item information."""
    
    filepath: str = f"data/receipts/{filename}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return Receipt.from_dict(json.load(f))
    raise FileNotFoundError(f"Coulnd't find '{filepath}.json' in `data/receipts/`!") 


def get_receipt_id(id: int) -> Receipt:
    """Returns a Receipt object based on stored data.
    
    :param id: int, the id of the stored receipt to return.
    
    :return receipt: Receipt, the Receipt like object to return containing item information."""

    return receipts_by_id[id]


def last_id() -> int:
    """Returns the latest (greatest) id of saved receipts"""
    receipts: List[Receipt] = get_receipts()
    return max([receipt.id for receipt in receipts])


# ******************************
# VARIABLES
# *******************************

receipts: List[Receipt] = get_receipts()
receipts_by_id: Dict[int, Receipt] = {receipt.id: receipt for receipt in receipts}
