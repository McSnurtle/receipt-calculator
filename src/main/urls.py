#src/main/urls.py
# imports
from typing import Any, Callable, Dict, Optional, Tuple, List
from src.main.views import index

from django.urls import path


# vars
urls: List[tuple[str, Any]] = [
    path("", index, name="index")
]