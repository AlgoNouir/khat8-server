from django.db import models
from Apps.Core.models import ReserveMainModel


class AcademyOrder(ReserveMainModel):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    birthday = models.IntegerField(blank=True, null=True)
    nationalCode = models.IntegerField(blank=True, null=True)