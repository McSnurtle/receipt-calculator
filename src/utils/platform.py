#src/utils/platform.py
# imports
import os
import pathlib
import json
from typing import Any, List, Dict
from .models import Receipt
from tkinter.messagebox import Message
from tkinter import Toplevel


def popup(title: str = "Popup Notification", message: str = "", icon: str = "info", options: str = "ok") -> str | None:
    """Display a universal popup notification with the specified message

    :param title: str, the title of the popup window to be displayed
    :param message: str, the body text of the popup to be displayed
    :param icon: str, the preset icon to use in the popup, valid options are: [error, info, question, warning]. This may vary depending on operating system
    :param options: str, the preset of response options for the user, valid options are: [ok, okcancel, retrycancel, yesno, yesnocancel]"""

    return Message(title=title, message=message, icon=icon, type=options).show()


# UNFINISHED!!!
def popup_input(title: str = "Popup Input", message: str = "") -> str | None:
    return ""


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
            
        
def get_receipt(name: str) -> Receipt | None:
    """Returns a Receipt object based on stored data.
    
    :param name: str, the filename of the receipt to check for excluding file types / extensions.
    
    :return receipt: Receipt, the Receipt like object to return containing item information. Returns None if the file does not exist."""
    
    filepath: str = f"data/receipts/{name}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return Receipt.from_dict(json.loads(f))
    return 
