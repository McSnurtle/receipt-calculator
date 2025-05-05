#/receiptcalculator/receipt/models.py
# imports
from typing import Any

from django.db import models
from django.db.models import CASCADE


# Create your models here.
class Receipt(models.Model):
    
    name: str | None | Any = models.CharField(max_length=200)
    payer: str | Any = models.CharField(max_length=20)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    
    parent = models.ForeignKey(Receipt, on_delete=CASCADE)
    buyer: str | Any = models.CharField()
    name: str | Any = models.CharField(max_length=200)
    cost: float | Any = models.FloatField(name)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.name