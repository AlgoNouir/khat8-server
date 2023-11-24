from django.db import models
from Apps.Core.models import ReserveMainModel


class CoffeeOrder(ReserveMainModel):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    desc = models.TextField(default="", max_length=40000)
