#src/utils/platform.py
# imports
import os
import json
from typing import Any
from tkinter.messagebox import Message

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



def get_conf(generate: bool = True) -> dict:
    """Returns a dictionary object of the configuration at `etc/conf.json`

    Args:
        generate (bool, optional): Whether to generate a new config file if one doesn't exist. Defaults to True.

    Returns:
        dict: The configuration dictionary object.
    """

    if not os.path.exists("etc/conf.json") and generate:
        generate_conf()
    with open("etc/conf.json", "r", encoding="utf-8") as f:
        return json.load(f)


def generate_conf() -> None:
    """Generates a new configuration file at `etc/conf.json` based on the defaults found in `etc/defaults.json`."""

    with open("etc/defaults.json", "r", encoding="utf-8") as source:
        with open("etc/conf.json", "w", encoding="utf-8") as target:
            target.write(source.read())


def get_version() -> str:
    """Returns a semver version derived from `etc/version.json`"""

    with open("etc/version.json", "r", encoding="utf-8") as f:
        return json.load(f)["version"]
