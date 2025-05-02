#receipt/urls.py
# imports
from typing import Any, Callable, Dict, Optional, Tuple, List
from . import views

from django.urls import path, URLPattern


# vars
urlpatterns: List[URLPattern] = [
    path("", views.index, name="index"),
    path("view", views.receipts, name="receipts"),
    path("create", views.create_receipt, name="create_receipt"),
    path("none", views.no_receipts, name="no_receipts"),
    path("delete/<int:receipt_id>", views.delete_receipt, name="delete_receipt")
]
