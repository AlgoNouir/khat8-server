from Apps.Core.models import MainModel
from django.db import models

# --------------------------------------------------------------------------+
#                                                                           |
#                                    Main                                   |
#                                                                           |
# --------------------------------------------------------------------------+


class Books(MainModel):
    class Meta:
        verbose_name_plural = "درخواست های انتشار"
    name = models.CharField(max_length=50, verbose_name="نام درخواست کننده", editable=False)
    mobNo = models.IntegerField(verbose_name="شماره تماس", editable=False)

    def __str__(self):
        return f"{self.name}-{self.mobNo}"

