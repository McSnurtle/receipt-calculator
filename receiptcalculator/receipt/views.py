#src/main/views.py
# imports
from typing import Any

from django.shortcuts import render, redirect
from django.http import HttpResponse

# webpages
def index(request: Any) -> Any:
    return HttpResponse("<h1>Welcome to the Django App!</h1>")

def receipts(request: Any) -> Any:
    return HttpResponse("<h1>Receipts</h1>")

def create_receipt(request: Any) -> Any:
    return HttpResponse("<h1>Create Receipt</h1>")

def no_receipts(request: Any) -> Any:
    return HttpResponse("<h1>No Receipts</h1>")

def delete_receipt(request: Any, receipt_id: int) -> Any:
    print(f"Deleting receipt with ID: {receipt_id}")
    return HttpResponse(f"<h1>Delete Receipt {receipt_id}</h1>")
