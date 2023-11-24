from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from Apps.Products.views import ProductView, ProductUserView, ProductRetreve
from Apps.User.views import UserView, CartView
from Apps.Orders.views import OrdersView
from Auth.views import LoginView
from Apps.Academy.views import AcademyView
from Apps.Caffeh.views import CoffeeView
from Apps.Fix.views import FixView
from Apps.Work.views import JobOfferView, JobRequestView


from Finance.views import sendRequest

urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", ProductView.as_view(), name="main"),
    path("productsUser/", ProductUserView.as_view(), name="mainUser"),
    path("product/retreve/", ProductRetreve.as_view(), name="retreve"),
    path("user/", UserView.as_view(), name="user"),
    path("login/", LoginView.as_view(), name="login"),
    path("user-refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("cart/", CartView.as_view(), name="cart"),
    path("order/", OrdersView.as_view(), name="order"),

    path("fix/", FixView.as_view(), name="fix"),
    path("coffee/", CoffeeView.as_view(), name="coffee"),
    path("academy/", AcademyView.as_view(), name="academy"),
    path("jobOffer/", JobOfferView.as_view(), name="jobOffer"),
    path("jobRequest/", JobRequestView.as_view(), name="jobRequest"),


    path("test/", sendRequest.as_view(), name="test"),
]
