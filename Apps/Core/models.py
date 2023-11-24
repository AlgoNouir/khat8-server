from django.db import models
from django.utils import timezone


class MainModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ReserveMainModel(MainModel):
    done = models.BooleanField(default=False)