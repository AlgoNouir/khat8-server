from Apps.User.models import CartItem, CartItemSerializer
from Apps.Orders.models import Order, OrderSerilizer
from django.db.models import Q
from Apps.Products.models import Category, Product, ProductSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions


class ProductView(APIView):
    # products/
    def get(self, request):
        """
        when an user open the web
        requested to this function

        this function return all product in database
        and user save that products on his redux

        this function is main function for this project
        becase just this function send data of products
        """

        products = Product.objects.all()
        products = ProductSerializer(products, many=True).data

        category = Category.objects.all()
        category = CategorySerializer(category, many=True).data
        response = {"products": products, "category": category, }

        return Response(response, status=status.HTTP_200_OK)

class ProductUserView(APIView):
    # products/
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        when an user open the web
        requested to this function

        this function return all product in database
        and user save that products on his redux

        this function is main function for this project
        becase just this function send data of products
        """

        # get all product data
        products = Product.objects.all()
        products = ProductSerializer(products, many=True).data

        # get category data
        category = Category.objects.all()
        category = CategorySerializer(category, many=True).data
        
        # get user cart data
        cart = CartItem.objects.filter(user__pk=request.user.pk)
        cart = CartItemSerializer(cart, many=True).data

        # get user cart data
        orders = Order.objects.filter(user__pk=request.user.pk).exclude(done=-1)
        orders = OrderSerilizer(orders, many=True).data
        
        response = {"products": products, "category": category, "cart":cart, "orders":orders}

        return Response(response, status=status.HTTP_200_OK)


class ProductRetreve(APIView):
    """
    data view
    """
    
    permission_classes=[permissions.AllowAny]

    def get(self, request):
        try:
            ID = request.GET["ID"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        product = Product.objects.get(id=ID)

        data = ProductSerializer(product).data

        return Response(data, status=status.HTTP_200_OK)