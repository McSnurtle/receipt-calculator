#src/utils/platform.py
# imports
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
