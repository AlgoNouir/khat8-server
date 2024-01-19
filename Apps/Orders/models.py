from django.db import models
from rest_framework.serializers import ModelSerializer
from melipayamak.melipayamak import Api
import sys
from Apps.Core.models import MainModel
from Apps.User.models import BaseUser
from Apps.Products.models import Product, KeeperCountItem

sys.setrecursionlimit(1500)

DONE_ENUM = [
    [-1, "پرداخت نشده"],
    [0, "در حال بررسی سفارش"],
    [1, "در حال آماده سازی"],
    [2, "ارسال شده"],
    [3, "سفارش انجام شده"],
]


class Order(MainModel):
    class Meta:
        verbose_name_plural = "سفارشات"
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, verbose_name="سفارش دهنده")
    done = models.SmallIntegerField("وضعیت سفارش", choices=DONE_ENUM, default=0)
    price = models.IntegerField("مبلغ سفارش")
    count = models.IntegerField("تعداد سفارش")
    postCode = models.CharField(
        "شماره پیگیری",
        max_length=50,
        blank=True, null=True, help_text="شماره پیگیری از اداره پست", )
    transactionAuthCode = models.CharField("کد درگاه پرداخت", max_length=100)

    def __str__(self):
        return f"{self.user.lName} {self.user.fName}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.done > 0 and self.postCode != None:
            print("ok i got data")

            api = Api("09210102710", 'EA!ROA0')
            sms_soap = api.sms('soap')
            res = sms_soap.send_by_base_number(
                f"{str(self.pk)};{str(self.postCode)}", f"0{self.user.phone}", 151607)
            # TODO print response of the sms


class OrderItem(MainModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سفارش")
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, verbose_name="کاربر")
    count = models.PositiveIntegerField(verbose_name="تعداد سبد خرید")
    # TODO merege this fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    select = models.ForeignKey(KeeperCountItem, on_delete=models.CASCADE, verbose_name="مدل انتخاب شده")


class OrderItemSerilizer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["count", "price", "product", "order", "select"]


class OrderSerilizer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["done", "price", "count", "created_at"]

    def to_representation(self, obj):
        data = super().to_representation(obj)

        data["products"] = OrderItemSerilizer(
            OrderItem.objects.filter(order__pk=obj.pk), many=True).data
        return data
