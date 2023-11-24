from django.shortcuts import render
from .models import CoffeeOrder
from melipayamak.melipayamak import Api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CoffeeView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        add order and reserve coffee shop

        Arg:
            request.data = {
                "name": name of person want to reserve or order
                "phone": phone of person want to reserve or order
                "desc": desc of person want to reserve or order
            }
        '''

        data = request.data
        order = CoffeeOrder(
            name=data['name'],
            phone=data["phone"],
            desc=data["desc"],
        )
        order.save()

        api = Api("09145970504", 'BG!RA')
        sms_soap = api.sms('soap')
        res = sms_soap.send_by_base_number(
            [str(order.pk)], f"0{data['phone']}", 151706)
        return Response(status=status.HTTP_201_CREATED)
