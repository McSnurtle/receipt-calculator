#src/utils/platform.py
# imports
import os
import pathlib
import json
from typing import Any, List, Dict
from .models import Receipt
from tkinter.messagebox import Message
from tkinter import Toplevel

# ********************
# FUNCTIONS
# ********************

def popup(title: str = "Popup Notification", message: str = "", icon: str = "info", options: str = "ok") -> str | None:
    """Display a universal popup notification with the specified message

    :param title: str, the title of the popup window to be displayed
    :param message: str, the body text of the popup to be displayed
    :param icon: str, the preset icon to use in the popup, valid options are: [error, info, question, warning]. This may vary depending on operating system
    :param options: str, the preset of response options for the user, valid options are: [ok, okcancel, retrycancel, yesno, yesnocancel]"""

    return Message(title=title, message=message, icon=icon, type=options).show()


def update_conf(key: str, value: Any) -> dict:
    """Updates the config found at `etc/conf.json` and writes it.
    
    :param key: str, the option to modify.
    :param value: Any, the value to set the option to.
    
    :return conf: dict, the configuration post-modification."""


    conf: dict = get_conf()
    conf[key] = value
    with open("etc/conf.json", "w") as f:
        payload: str = json.dumps(conf)
        f.write(payload)
    return conf


def get_conf() -> dict:
    """Returns a dictionary object of the configuration at `etc/conf.json`"""
    
    with open("etc/conf.json", "r") as f:
        return json.load(f)
    
    
def get_version() -> str:
    """Returns a semver version derived from `etc/version.json`"""
    
    with open("etc/version.json", "r") as f:
        return json.load(f)["version"]
