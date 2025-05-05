from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    # view all receipts and their calculations
    path("add/", views.add_receipt, name="add_receipt"),
    path("<int:receipt_id>/", views.receipt_detail, name="receipt_detail"),
    # path("<int:receipt_id>/delete/", views.delete_receipt, name="delete_receipt"),    # THIS SHOULD BE A REQUEST ON THE EDIT PAGE, NOT IT'S OWN PAGE!!
    path("<int:receipt_id>/edit/", views.edit_receipt, name="edit_receipt"),
]
