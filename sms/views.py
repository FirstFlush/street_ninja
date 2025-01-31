from django.shortcuts import render
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Request, Response, status
from geo.geocoding import GeocodingService

from twilio.twiml.messaging_response import MessagingResponse
from auth.authentication import TwilioSignatureAuthentication
from .serializers import TwilioSMSSerializer


class SMSWebhookView(APIView):

    # authentication_classes = [TwilioSignatureAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]

    def post(self, request:Request, *args, **kwargs):

        # geocoding_service = GeocodingService()
        # location = geocoding_service.geocode(query="688 Abbott St, Vancouver, BC, Canada")
        # print(location)
        # res = MessagingResponse()
        # print(res.message("this is a test text kakaka \nheloooo"))
        # print("data: ") 
        # print(request.data)
        # print("-"*50)
        print(request.data)
        print()
        deserializer = TwilioSMSSerializer(data=request.data)
        if deserializer.is_valid():
            print(deserializer.validated_data)
        else:
            print(deserializer.errors)


        return Response("fasdfasd", status=status.HTTP_200_OK)