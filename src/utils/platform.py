#src/utils/platform.py
# imports
import os
import json


def get_local_version() -> str:
    """Returns the local, current version of the software. e.g. 'v0.0.0'."""
    with open("etc/version.json", "r") as file:
        return json.load(file)
    