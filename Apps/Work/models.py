from django.db import models
from Apps.Core.models import ReserveMainModel


class JobOffer(ReserveMainModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    landlinePhone = models.IntegerField()
    organName = models.CharField(max_length=50)
    organWork = models.CharField(max_length=50)
    cityName = models.CharField(max_length=50)
    provinceName = models.CharField(max_length=50)



class JobRequest(ReserveMainModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    landlinePhone = models.IntegerField()
    organName = models.CharField(max_length=50)
    organWork = models.CharField(max_length=50)
    cityName = models.CharField(max_length=50)
    provinceName = models.CharField(max_length=50)
    edjLevel = models.CharField(max_length=50)
    edjField = models.CharField(max_length=50)
    desc = models.TextField(max_length=2000)
