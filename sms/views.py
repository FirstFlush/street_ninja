from django.shortcuts import render
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Request, Response, status
from geo.geocoding import GeocodingService

from twilio.twiml.messaging_response import MessagingResponse
from auth.authentication import TwilioSignatureAuthentication
from .serializers import TwilioSMSSerializer
from .sms_service import SMSService
from .resolvers import SMSResolver


class SMSWebhookView(APIView):

    # authentication_classes = [TwilioSignatureAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]

    def post(self, request:Request, *args, **kwargs):

        print(request.data)
        print()
        deserializer = TwilioSMSSerializer(data=request.data)
        if deserializer.is_valid():
            SMSService(
                resolver=SMSResolver(deserializer.validated_data['Body'])
            )
        else:
            print(deserializer.errors)


        return Response("fasdfasd", status=status.HTTP_200_OK)