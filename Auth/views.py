from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Apps.User.models import UserSerializer, CartItem
from Apps.Orders.models import Order, OrderSerilizer, OrderItem, OrderItemSerilizer
from Apps.Products.models import Product, KeeperCountItem

from melipayamak.melipayamak import Api
from random import randint

User = get_user_model()


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        request for when user want to send sms
        if code in user send it here and
        verify code sended with phone

        TODO send the sms code to phone number
        TODO validate phone number
        TODO if user update is less than 10 min accepted
        TODO this function work with redis

        Arg :
            request.data = {
                'phone' : phone number that we send the sms
                'code' : what code sended
            }
        """
        data = request.data

        try:
            person = User.objects.get(phone=data["phone"])
        except Exception:
            if "code" not in list(data.keys()):
                print("person not found creating new person")
                person = User(phone=data["phone"])
            else:  # return the true code for hackers not found mobile in database
                return Response(status=status.HTTP_205_RESET_CONTENT)

        if "code" not in list(data.keys()):
            password = str(randint(100000, 999999))
            api = Api("09210102710", 'EA!ROA0')
            sms_soap = api.sms('soap')
            res = sms_soap.send_by_base_number(
                [password], f"0{person.phone}", 151469)
            print(password)
            person.password = password

            person.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        if person.password != str(data["code"]):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        for p in data["products"]:
            # {'id': -1, 'product': 1, 'select': 1, 'count': 5}
            try:

                cartItem = CartItem(
                    user=person,
                    select=KeeperCountItem.objects.get(pk=p["select"]),
                    product=Product.objects.get(pk=p["product"]),
                    count=p["count"]
                )

                cartItem.save()
            except:
                cartItem = CartItem.objects.get(
                    user=person,
                    select=KeeperCountItem.objects.get(pk=p["select"])
                )
                cartItem.count = p["count"]
                cartItem.save()

        refresh = RefreshToken.for_user(person)
        orders = Order.objects.filter(user=person).exclude(done=-1)
        person = UserSerializer(person)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": person.data,
            "orders": OrderSerilizer(orders, many=True).data,
        }

        return Response(data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        user = UserSerializer(self.user)

        data.update({"user": user.data})

        return data


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
