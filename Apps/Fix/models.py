from django.db import models
from Apps.Core.models import ReserveMainModel


class FixOrder(ReserveMainModel):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()