from django.shortcuts import render
from .models import AcademyOrder
from melipayamak.melipayamak import Api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AcademyView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        add order and reserve coffee shop

        Arg:
            request.data = {
                "name"(str): name of person want to reserve or order
                "phone"(int): phone of person want to reserve or order
                "birthday"(int): birthday of person want to reserve or order
                "nationalCode"(int): nationalCode of person want to reserve or order
            }
        '''

        data = request.data
        order = AcademyOrder(
            name=data['name'],
            phone=data["phone"],
            birthday=data["birthday"],
            nationalCode=data["nationalCode"],
        )
        order.save()

        api = Api("09145970504", 'BG!RA')
        sms_soap = api.sms('soap')
        res = sms_soap.send_by_base_number(
            [str(order.pk)], f"0{data['phone']}", 151709)
        return Response(status=status.HTTP_201_CREATED)
