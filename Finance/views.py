from django.conf import settings
from django.db.models import Sum, F
from Apps.User.models import CartItem, BaseUser
from rest_framework.response import Response
from Apps.Orders.models import Order
from rest_framework.views import APIView
from rest_framework import status

import requests
import json


if settings.DEBUG:
    first = "sandbox"
else:
    first = "www"


# TODO: set sandbox to real
ZP_API_REQUEST = f"https://{first}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{first}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{first}.zarinpal.com/pg/StartPay/"


class sendRequest(APIView):

    def post(self, request, *args, **kwargs):

        items = CartItem.objects.filter(user=request.user.pk)

        price = 0
        count = 0
        postPrice = 45000
        for item in items:

            # userCartItem = CartItem.objects.filter(user=order.user)
            # for cartItem in userCartItem:
            #     if cartItem.count > cartItem.product.countCanBuy:
            #         return Response(status=status.HTTP_400_BAD_REQUEST)
            #     if cartItem.count > cartItem.select.amount:
            #         return Response(status=status.HTTP_400_BAD_REQUEST)

            if item.product.category.pk in [61]:
                postPrice = 0
            if item.product.offerPrice == 0:
                price += item.count * item.product.price
            else:
                price += item.count * item.product.offerPrice
            count += 1

        print(settings.WHOAMI + "order")

        if (price != 0):
            price += postPrice
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": price,
                "Description": "سفارش شما از وبسایت فروشگاهی و مجموعه خدماتی - تجاری - کارنسینو",
                "Phone": request.user.phone,
                "CallbackURL": "https://currencyno-server.iran.liara.run/order",
            }
            data = json.dumps(data)

            # set content length by data
            try:
                print("start getway for payment")
                response = requests.post(
                    ZP_API_REQUEST,
                    data=data,
                    headers={'content-type': 'application/json',
                             'content-length': str(len(data))},
                    timeout=10
                )

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        order = Order(
                            done=-1,
                            user=request.user,
                            price=price,
                            transactionAuthCode=response["Authority"],
                            count=count,
                        )
                        order.save()
                        return Response({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']})
                    else:
                        return Response({'error': str(response['Status'])}, status=status.HTTP_510_NOT_EXTENDED)
                print("i am in test")
                return Response(response)

            except requests.exceptions.Timeout:
                return Response(status=status.HTTP_504_GATEWAY_TIMEOUT)
            except requests.exceptions.ConnectionError:
                return Response(status=status.HTTP_502_BAD_GATEWAY)
            except Exception as e:
                print(e)

        return Response(status=status.HTTP_400_BAD_REQUEST)


def verifyTransaction(authority, price):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": price,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json',
               'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    print(response)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return True
        else:
            return False
    else:
        return False
