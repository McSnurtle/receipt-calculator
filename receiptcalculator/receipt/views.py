#receiptcalculator/reciept/views.py
# imports
from typing import Any

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request: Any):
    return HttpResponse("<h1>Receipt Calculator</h1><p>Welcome to the Receipt Calculator!</p>")

def receipt_detail(request: Any, receipt_id: int):
    return HttpResponse(f"<h1>Receipt Details</h1><p>Details for receipt {receipt_id}</p>")

def edit_receipt(request: Any, receipt_id: int):
    return HttpResponse(f"<h1>Edit Receipt</h1><p>Editing content of receipt {receipt_id}</p>")

def add_receipt(request: Any):
    return HttpResponse(f"<h1>Add Receipt</h1>")

def no_receipts(request: Any):
    return HttpResponse(f"<h1>No Receipts</h1><p>Would you like to create one now?</p>")

# def delete_receipt(request: Any, receipt_id: int):
#     return HttpResponse(f"<h1>Delete {receipt_id}</h1>")