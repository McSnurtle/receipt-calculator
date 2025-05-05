#src/main.py
# imports
import os
import json
import tkinter as tk
from typing import Any

from utils.platform import popup

# vars
pass


class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        