from Apps.Core.models import MainModel
from Apps.Products.models import Product, KeeperCountItem
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from rest_framework.serializers import ModelSerializer


class BaseUserManager(BUM):
    def create_user(
        self,
        phone,
        fName=None,
        lName=None,
        address=None,
        lat=None,
        long=None,
        email=None,
        nationalCode=None,
        password=None,
        is_active=True,
        is_admin=False,
    ):
        if not phone:
            raise ValueError("Users must have an uniqe phone_number")

        user = self.model(
            phone=phone,
            fName=fName,
            lName=lName,
            address=address,
            lat=lat,
            long=long,
            email=email,
            nationalCode=nationalCode,
            password=password,
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, *args, **kwargs):
        user = self.create_user(
            phone=phone,
            fName="",
            lName="",
            address="",
            lat=1,
            long=1,
            email="",
            nationalCode=1,
            password=password,
            is_active=True,
            is_admin=True,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(MainModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "کاربران"
    phone = models.IntegerField(unique=True, verbose_name="شماره تلفن مشتری")

    fName = models.CharField(null=True, blank=True,
                             max_length=50, verbose_name="نام شخص")

    lName = models.CharField(
        null=True, blank=True, max_length=50, verbose_name="نام خانوادگی شخص"
    )

    address = models.TextField(
        null=True, blank=True, max_length=200, verbose_name="آدرس محل سکونت"
    )

    lat = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="طول جغرافیایی محل سکونت شخص"
    )

    long = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="عرض جغرافیایی محل سکونت شخص"
    )

    email = models.CharField(
        null=True, blank=True, max_length=50, verbose_name="ایمیل شخص"
    )

    nationalCode = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="کد پستی"
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.pk} , {self.phone}"

    def is_staff(self):
        return self.is_admin


# class MessageModel(BaseModel):
#     user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     desc = models.TextField(max_length=300)
#     url = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.name} - {self.title}"


# class MessageSerializer(ModelSerializer):
#     class Meta:
#         model = MessageModel
#         exclude = [
#             "user",
#             "created_at",
#             "updated_at"
#         ]

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['date'] = instance.created_at
#         return data


OrderStatusEnum = [[0, "در سبد خرید"], [1, "در سفارش"]]


class CartItem(MainModel):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, verbose_name="کاربر")
    count = models.PositiveIntegerField(verbose_name="تعداد سبد خرید")
    # TODO merege this fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    select = models.ForeignKey(KeeperCountItem, on_delete=models.CASCADE, verbose_name="مدل انتخاب شده")

    class Meta:
        verbose_name_plural = "سبد خرید"
        unique_together = ('select', 'user',)


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ["created_at", "updated_at", "user"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        exclude = [
            "password",
            "created_at",
            "updated_at",
            "is_superuser",
            "is_active",
            "is_admin",
            "groups",
            "user_permissions",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["products"] = CartItemSerializer(
            CartItem.objects.filter(user__pk=instance.pk), many=True
        ).data

        return data
