#src/utils/models.py
"""Contains classes or 'models' for the datastructures / data types stored by the project

Raises:
    ValueError: if Item.from_dict() is ran with incompatible dictionary keys / values
    TypeError: if Receipt.from_dict() is ran with incompatible dictionary keys / values

Returns:
    None: N/A
"""
# imports
import json
from typing import Any, Dict, List, Union
from .id_generator import last_id   # type: ignore
from .platform_specific import get_conf   # type: ignore


class Item(Dict[str, Any]):
    """A purchased item to be tracked on a Receipt object.

        :param name: str, the name / description of the item that was purchased.
        :param user: str, the name of the person who the item is / was for.
        :param cost: float, the base cost of the item purchased *not* including taxes or fees.
        :param tax: float | None, OPTIONAL, the tax applied to the item purchased. If None, will use the default tax from the config file.
        :param should_tax: bool, whether this item has tax applied to it or not in calculations.
        """

    def __init__(self, name: str, user: str, cost: float, tax: float | None = None, tip: float | None = None, should_tax: bool = True):

        self.name: str = name
        self.user: str = user
        self.cost: float = cost
        self.tax: float = tax if tax is not None else get_conf()["defaultTax"]
        self.tip: float = tip if tip is not None else 0.0
        self.should_tax: bool = should_tax

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Union[Dict[str, Any], object]:
        """Creates a new Receipt object with it's data fields derived from a custom dictionary

        Args:
            data (dict[str, Any]): the dictionary to pull receipt info from

        Returns:
              object: an Item object instantiated from the provided custom dictionary's values
        """

        try:
            item: Item = Item(data["name"], data["user"], data["cost"], data["tax"], data["tip"], data["shouldTax"])
        except KeyError as e:
            raise ValueError(f"Got unexpected item param: {e}\n - `data` should have `name`: str, `user`: str, `cost`: float, `tax`: float, `tip`: float, `should_tax`: bool!") from e
        return item

    def to_dict(self) -> Dict[str, Any]:
        """Returns the item object as a standard dictionary.

        Returns:
              Dict[str, Any]: The item objects fields as a dictionary: `name`, `user`, `cost`, and `should_tax`.
        """

        return {
            "name": self.name,
            "user": self.user,
            "cost": self.cost,
            "should_tax": self.should_tax
        }


# NOTE: Added object as a type stored by Receipt to stop PyLint from complaining about appending Item.from_dict() which returns object
class Receipt(List[Union[Item, object]]):
    """A receipt tracking all child Item objects.

    :param name: str, the name of the receipt - used solely for end-user.
    :param buyer: str, the name of the person who paid for all items on the receipt.
    :param payee: str | None, OPTIONAL, the company / person the receipt is from.
    :param date: str | None, OPTIONAL, the date + time the receipt / purchase was made - used soley for end-user.
    """

    def __init__(self, name: str, buyer: str, payee: str | None, date: str | None, new: bool = False):

        self.name: str = name
        self.id = last_id()
        if new:
            self.id += 1
        self.buyer: str = buyer
        self.payee: str | None = payee
        self.date: str | None = date

    @property
    def items(self) -> List[Union[Item, object]]:
        """Returns the list of items in the receipt."""
        return self.copy()

    @property
    def people(self) -> List[str]:
        """Returns a list of all people who are on the receipt."""
        people: List[str] = []
        for item in self:
            if isinstance(item, Item) and item.user not in people:
                people.append(item.user)
        return people

    @staticmethod
    def from_dict(data: Union[Dict[str, Any], Any]) -> Union[List[Item], object]:
        """Instantiates a new Receipt object based on the custom dictionary provided.

        Args:
            data (Dict[str, Any]): the dictionary with the custom receipt values.

        Raises:
            TypeError: if the values do not follow: `name`: str, `buyer`: str, `payee`: str, `date`: datetime.datetime, and `items`: List[Item]!

        Returns:
            List[Item]: the Receipt object that is returned
        """
        try:
            receipt: Receipt = Receipt(name=data['name'], buyer=data['buyer'], payee=data['payee'], date=data['date'])
            for item in data["items"]:
                receipt.append(Item.from_dict(item))
                receipt.id = data["id"]
        except KeyError as e:
            raise TypeError(f'Got unexpected receipt param {e}\n - `data` should have `name`: str, `buyer`: str, `payee`: str, `date`: datetime.datetime, and `items`: List[Item]!') from e
        return receipt

    @staticmethod
    def from_file(file: Any) -> List[Union[List, object]]:
        """Creates a new Receipt object based on file contents.

        Args:
            file (Union[SupportsRead[str | bytes], IO[Incomplete]]): the file contents to parse.

        Raises:
            TypeError: _description_

        Returns:
            List[Item]: _description_
        """

        data = json.load(file)
        try:
            receipt: Receipt = Receipt(name=data["name"], buyer=data["buyer"], payee=data["payee"], date=data["date"])
            for item in [_ for _ in data["items"] if isinstance(_, dict)]:
                receipt.append(Item.from_dict(item))
                receipt.id = data["id"]
        except KeyError as e:
            raise TypeError(f"Got unexpected receipt param {e}\n - `data` should have `name`: str, `buyer`: str, `payee`: str, `date`: datetime.datetime, and `items`: List[Item]!") from e
        return receipt

    def to_dict(self) -> Dict[str, Any]:
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
