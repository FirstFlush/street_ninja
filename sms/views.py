import logging
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Request, Response, status
from geo.geocoding import GeocodingService

from twilio.twiml.messaging_response import MessagingResponse
from auth.authentication import TwilioSignatureAuthentication
from .serializers import TwilioSMSSerializer
from .sms_service import SMSService
from .resolvers import SMSResolver


logger = logging.getLogger(__name__)

class SMSWebhookView(APIView):

    # authentication_classes = [TwilioSignatureAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]

    def post(self, request:Request, *args, **kwargs):

        deserializer = TwilioSMSSerializer(data=request.data)
        if deserializer.is_valid():
            sms_service = SMSService(
                msg=deserializer.validated_data["Body"],
                phone_number=deserializer.validated_data["From"],
                message_sid=deserializer.validated_data["MessageSid"],
            )
            sms_service.process_sms()
        else:
            logger.error(f"Failed to deserialize: {deserializer.errors}")
            return Response("Could not parse message", status=status.HTTP_400_BAD_REQUEST)

        return Response("fasdfasd", status=status.HTTP_200_OK)