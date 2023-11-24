from django.shortcuts import render
from .models import JobOffer, JobRequest
from melipayamak.melipayamak import Api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class JobOfferView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        add order and reserve coffee shop

        Arg:
            request.data = {
                "name" : name of job offer boss
                "email" : email of job offer boss 
                "phone" : phone number of job offer boss 
                "landlinePhone" : shmare tamas of job offer boss 
                "organName" : name of job offer organ 
                "organWork" : name of job offer organ work 
                "cityName" : name of job offer organ city 
                "provinceName" : name of job offer organ ostan 
            }
        '''

        data = request.data
        order = JobOffer(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            landlinePhone=data["landlinePhone"],
            organName=data["organName"],
            organWork=data["organWork"],
            cityName=data["cityName"],
            provinceName=data["provinceName"]
        )
        order.save()

        api = Api("09145970504", 'BG!RA')
        sms_soap = api.sms('soap')
        res = sms_soap.send_by_base_number(
            [str(order.pk)], f"0{data['phone']}", 151715)
        return Response(status=status.HTTP_201_CREATED)


class JobRequestView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        add order and reserve coffee shop

        Arg:
            request.data = {
                "name" : name of job request person
                "email" : email of job request person 
                "phone" : phone number of job request person 
                "landlinePhone" : shmare tamas of job request person 
                "cityName" : name of job request organ city 
                "provinceName" : name of job request organ ostan 
                "edjLevel" : edjLevel of job request
                "edjField" : edjField of job request
                "desc" : desc of job request
            }
        '''

        data = request.data
        jobRequest = JobRequest(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            landlinePhone=data["landlinePhone"],
            cityName=data["cityName"],
            provinceName=data["provinceName"],
            edjLevel=data['edjLevel'],
            edjField=data['edjField'],
            desc=data['desc']
        )
        jobRequest.save()

        # TODO set SMS
        return Response(status=status.HTTP_201_CREATED)
