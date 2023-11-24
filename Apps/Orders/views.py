from django.conf import settings
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from Apps.User.models import BaseUser, CartItem
from Apps.Products.models import Product, KeeperCountItem
from .models import Order, OrderItem


from melipayamak.melipayamak import Api
from Finance.views import verifyTransaction

# order/


class OrdersView(APIView):
    def get(self, requeset):
        """
        when zarinpal response set data
        this function run
        set cart items to new order

        Arg:
            request.user = user who want do this work
            request.GET = {
                Authority : transaction auth code
                Status : status of transaction
            }

        """

        order = Order.objects.get(
            transactionAuthCode=requeset.GET["Authority"])

        if verifyTransaction(requeset.GET["Authority"], order.price):
            order.done = 0
            user = order.user
            for cartItem in CartItem.objects.filter(user__pk=user.pk):
                # cart Item now price
                price = (
                    cartItem.product.price - cartItem.product.offerPrice
                ) * cartItem.count

                # create order item
                orderItem = OrderItem(
                    order=order,
                    price=price,
                    product=cartItem.product,
                    count=cartItem.count,
                    select=cartItem.select,
                )

                keeperCountItem = KeeperCountItem.objects.get(
                    pk=cartItem.select.pk)
                keeperCountItem.amount -= cartItem.count
                keeperCountItem.save()

                # change order data
                order.count = cartItem.count

                orderItem.save()
                cartItem.delete()
            order.save()
            api = Api("09145970504", 'BG!RA')
            sms_soap = api.sms('soap')
            res = sms_soap.send_by_base_number(
                [str(order.pk)], f"0{user.phone}", 151605)
            # TODO print response of the sms

            print(f"order added for person {order.user.phone}")
        return redirect("https://currencyno.com/")
