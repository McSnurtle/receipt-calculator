#src/main/views.py
# imports
from typing import Any

from django.shortcuts import render, redirect
from django.http import HttpResponse

# views
def index(request: Any) -> Any:
    return HttpResponse("<h1>Welcome to the Django App!</h1>")
