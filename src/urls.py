#src/urls.py
# imports
from typing import Any, Callable, Dict, Optional, Tuple, List
from django.urls import path, include

urlpatterns: List[Tuple[str, Any]] = [
    path("admin/", include("admin.urls")),
    path("", include("main.urls")),
]
