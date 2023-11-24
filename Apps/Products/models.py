from Apps.Core.models import MainModel
from rest_framework.serializers import ModelSerializer
from django.db import models

# --------------------------------------------------------------------------+
#                                                                           |
#                                 Category                                  |
#                                                                           |
# --------------------------------------------------------------------------+


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.CASCADE
    )
    # havePostPrice = models.BooleanField(default=True, help_text="برای حذف هزینه پستی در این دسته بندی تیک را بردارید")
    

    def __str__(self):
        return self.name


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# --------------------------------------------------------------------------+
#                                                                           |
#                                    Data                                   |
#                                                                           |
# --------------------------------------------------------------------------+

DELIVERY_ENUM = [[0, "تحویل با پست"]]


class ProdutData(models.Model):
    name = models.CharField(max_length=50, help_text="نام ویژگی محصول")
    amount = models.CharField(max_length=50, help_text="مقدار ویژگی محصول")

    def __str__(self) -> str:
        return f"{self.name} - {self.amount}"


# --------------------------------------------------------------------------+
#                                                                           |
#                                    Main                                   |
#                                                                           |
# --------------------------------------------------------------------------+


class Product(MainModel):
    garanty = models.CharField(max_length=50, help_text="شرایط گارانتی")
    persianName = models.CharField(max_length=50, help_text="نام فارسی محصول")
    price = models.IntegerField(help_text="قیمت محصول")
    data = models.ManyToManyField(ProdutData)
    englishName = models.CharField(
        max_length=50, help_text="نام انگلیسی محصول")
    desc = models.TextField(max_length=2000, help_text="توضیحات محصول")
    original = models.BooleanField(default=False)
    deliveryType = models.IntegerField(
        choices=DELIVERY_ENUM, help_text="نوع تحویل محصول"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, help_text="دسته بندی"
    )
    offerPrice = models.IntegerField(
        default=0, help_text="میزان تخفیف محصول (صفر به معنای بدون تخفیف)"
    )
    countCanBuy = models.PositiveIntegerField(
        default=0,
        help_text="هر کاربر به چه تعداد از این محصول می تواند بخرد؟ (صفر به معنای آزاد)",
    )

    def __str__(self):
        return self.persianName


# --------------------------------------------------------------------------+
#                                                                           |
#                                   Items                                   |
#                                                                           |
# --------------------------------------------------------------------------+


class KeeperCountItem(models.Model):
    name = models.CharField(max_length=50, help_text="نام ویژگی محصول")
    amount = models.IntegerField(help_text="مقدار ویژگی محصول")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, help_text="محصولی که این مقدار برای آن است."
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.amount}"


class ProductImage(models.Model):
    image = models.CharField(
        help_text="آدرس سرور ارائه دهنده عکس", max_length=50)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, help_text="این عکس مربوط به کدام محصول است؟"
    )

    def __str__(self):
        return f"عکس {self.product.persianName}"


# --------------------------------------------------------------------------+
#                                                                           |
#                                Serializers                                |
#                                                                           |
# --------------------------------------------------------------------------+


class KeeperCountItemSerializer(ModelSerializer):
    class Meta:
        model = KeeperCountItem
        exclude = ["product"]


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]

    def to_representation(self, instance):
        return instance.image


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "data"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["image"] = ProductImageSerializer(
            ProductImage.objects.filter(product=instance.pk), many=True
        ).data
        data["data"] = {}
        for d in instance.data.all():
            data["data"][d.name] = d.amount

        data["counts"] = KeeperCountItemSerializer(
            KeeperCountItem.objects.filter(product__pk=instance.pk), many=True
        ).data

        return data

