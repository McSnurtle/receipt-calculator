#src/utils/models.py
# imports
import os
import json
import typing
from datetime import datetime
from typing import Any, Dict, List, IO, Union
from .receipts import last_id


class Item(Dict[str, Any]):
    def __init__(self, name: str, user: str, cost: float, should_tax: bool = True):
        """A purchased item to be tracked on a Receipt object.
        
        :param name: str, the name / description of the item that was purchased.
        :param user: str, the name of the person who the item is / was for.
        :param cost: float, the base cost of the item purchased *not* including taxes or fees.
        :param should_tax: bool, whether this item has tax applied to it or not in calculations.
        """

        self.name: str = name
        self.user: str = user
        self.cost: float = cost
        self.should_tax: bool = should_tax

    @staticmethod
    def from_dict(data: dict) -> Dict[str, Any]:
        item: Item = Item("", "", "", "")
        try:
            item.name = data["name"]
            item.user = data["user"]
            item.cost = data["cost"]
            item.should_tax = data["should_tax"]
        except KeyError as e:
            print(f"Got unexpected item param: {e}\n - `data` should have `name`: str, `user`: str, `cost`: float, and `should_tax`: bool!")
        return item
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "user": self.user,
            "cost": self.cost,
            "should_tax": self.should_tax
        }


class Receipt(List[Item]):
    def __init__(self, name: str, buyer: str, payee: str | None, date: str | None):
        """A receipt tracking all child Item objects.

        :param name: str, the name of the receipt - used solely for end-user.
        :param buyer: str, the name of the person who paid for all items on the receipt.
        :param payee: str | None, OPTIONAL, the company / person the receipt is from.
        :param date: str | None, OPTIONAL, the date + time the receipt / purchase was made - used soley for end-user.
        """

        self.name: str = name
        self.buyer: str = buyer
        self.payee: str | None = payee
        self.date: str | None = date

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> List[Item]:
        try:
            receipt: Receipt = Receipt(name=data['name'], buyer=data['buyer'], payee=data['payee'], date=data['date'])
            for item in data["items"]:
                receipt.append(Item.from_dict(item))
        except KeyError as e:
            raise TypeError(f"Got unexpected receipt param {e}\n - `data` should have `name`: str, `buyer`: str, `payee`: str, `date`: datetime.datetime, and `items`: List[Item]!")
        return receipt
    
    @staticmethod
    def from_file(file: 'Union[SupportsRead[str | bytes], IO[Incomplete]]') -> List[Item]:
        data = json.load(file)
        try:
            receipt: Receipt = Receipt(name=data["name"], buyer=data["buyer"], payee=data["payee"], date=data["date"])
            for item in [_ for _ in data["items"] if isinstance(_, dict)]:
                receipt.append(Item.from_dict(item))
        except KeyError as e:
            raise TypeError(f"Got unexpected receipt param {e}\n - `data` should have `name`: str, `buyer`: str, `payee`: str, `date`: datetime.datetime, and `items`: List[Item]!")
        return receipt

    def to_dict(self) -> Dict:
        """Returns a dictionary-like object containing the data from the receipt."""
        return {
            "name": self.name,
            "buyer": self.buyer,
            "payee": self.payee,
            "date": self.date,
            "items": self.copy()    # <== should return Item objects which are stored in the list only
        }
    
    def __str__(self) -> str:
        return self.name
