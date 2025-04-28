#src/main.py
# imports
import json
import os
import sys
from utils.platform import get_local_version

from flask import Flask


class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
if __name__ == "__main__":
    app = App()
    app.run(debug=True)
    