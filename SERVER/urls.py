from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from Apps.Products.views import ProductView, ProductUserView, ProductRetreve
from Apps.User.views import UserView, CartView
from Apps.Orders.views import OrdersView
from Auth.views import LoginView
from Apps.Books.views import BookView


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
    path("book", BookView.as_view(), name="book"),

    path("test/", sendRequest.as_view(), name="test"),
]
