from django.shortcuts import render
from .models import FixOrder
from melipayamak.melipayamak import Api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FixView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        add order and reserve coffee shop

        Arg:
            request.data = {
                "name": name of person want to reserve or order
                "phone": phone of person want to reserve or order
            }
        '''

        data = request.data
        order = FixOrder(
            name=data['name'],
            phone=data["phone"],
        )
        order.save()

        api = Api("09145970504", 'BG!RA')
        sms_soap = api.sms('soap')
        res = sms_soap.send_by_base_number(
            [str(order.pk)], f"0{data['phone']}", 151711)
        return Response(status=status.HTTP_201_CREATED)
