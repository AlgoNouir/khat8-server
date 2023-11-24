from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.admin import UserAdmin
from Apps.Products.models import (
    Product,
    Category,
    ProductImage,
    ProdutData,
    KeeperCountItem,
)
from Apps.User.models import BaseUser, CartItem
from Apps.Orders.models import Order, OrderItem

from Apps.Fix.models import FixOrder
from Apps.Work.models import JobOffer, JobRequest
from Apps.Academy.models import AcademyOrder
from Apps.Caffeh.models import CoffeeOrder

admin.site.register(Category)
admin.site.register(ProdutData)
admin.site.register(CartItem)


class OrderItemInline(admin.TabularInline):
    verbose_name_plural = "سفارش های آیتم"
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ["done"]
    search_fields = ["user__phone"]
    list_display = ["id", "user", "price", "count", "done"]
    readonly_fields = ('id',)
    inlines = [OrderItemInline]


@admin.register(BaseUser)
class ProductAdmin(UserAdmin):
    list_filter = ["is_admin"]
    ordering = ["phone"]
    search_fields = ["fName", "lName", "nationalCode"]
    list_display = ["phone", "fName", "lName", "is_admin"]
    fieldsets = [
        (
            "مشخصات محصول",
            {
                "fields": [
                    "phone",
                    "fName",
                    "password",
                    "lName",
                    "address",
                    "lat",
                    "long",
                    "email",
                    "nationalCode",
                    "is_active",
                    "is_admin",
                ]
            },
        ),
    ]

    add_fieldsets = [
        (
            "مشخصات محصول",
            {
                "fields": [
                    "phone",
                    "fName",
                    "password1",
                    "password2",
                    "lName",
                    "address",
                    "lat",
                    "long",
                    "email",
                    "nationalCode",
                    "is_active",
                    "is_admin",
                ]
            },
        ),
    ]


class ProductImagesInline(admin.TabularInline):
    verbose_name_plural = "عکس های محصول"
    model = ProductImage


class KeeperCountItemInline(admin.TabularInline):
    verbose_name_plural = "موجودی انباری"
    model = KeeperCountItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ["original"]
    search_fields = ["persianName"]
    list_display = ["persianName", "original", "price", "offerPrice"]
    inlines = [ProductImagesInline, KeeperCountItemInline]
    filter_horizontal = ('data',)

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     vertical = False  # change to True if you prefer boxes to be stacked vertically
    #     kwargs['widget'] = widgets.FilteredSelectMultiple(
    #         db_field.verbose_name,
    #         vertical,
    #     )
    #     return super(MyModelAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets = [
        (
            "مشخصات محصول",
            {
                "fields": (
                    "category",
                    "persianName",
                    "englishName",
                    "desc",
                    "original",
                    "data",
                ),
            },
        ),
        (
            "شرایط خرید",
            {
                "fields": (
                    "price",
                    "deliveryType",
                    "countCanBuy",
                    "offerPrice",
                    "garanty",
                ),
            },
        ),
    ]

    add_fieldsets = [
        (
            "مشخصات محصول",
            {
                "fields": (
                    "category",
                    "persianName",
                    "englishName",
                    "desc",
                    "original",
                    "data",
                ),
            },
        ),
        (
            "شرایط خرید",
            {
                "fields": (
                    "price",
                    "deliveryType",
                    "countCanBuy",
                    "offerPrice",
                    "garanty",
                ),
            },
        ),
    ]


@admin.register(FixOrder)
class FixOrderAdmin(admin.ModelAdmin):
    list_filter = ["done"]
    search_fields = ["name", "phone"]
    list_display = ["name", "phone", "done"]


@admin.register(CoffeeOrder)
class CoffeeOrderAdmin(admin.ModelAdmin):
    list_filter = ["done"]
    search_fields = ["name", "phone"]
    list_display = ["name", "phone", "done"]


@admin.register(AcademyOrder)
class AcademyOrderAdmin(admin.ModelAdmin):
    list_filter = ["done"]
    search_fields = ["name", "phone"]
    list_display = ["name", "phone", "done"]


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_filter = ["done"]
    search_fields = ["name", "phone"]
    list_display = ["name", "phone", "done"]


@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_filter = ["done"]
    search_fields = ["name", "phone"]
    list_display = ["name", "phone", "done"]
