import logging
from django.conf import settings
from django.http import HttpResponse
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Request, Response, status
from twilio.twiml.messaging_response import MessagingResponse
from auth.authentication import TwilioSignatureAuthentication
from .serializers import TwilioSMSSerializer, WebSMSSerializer
from .sms_service import SMSService
from sms.response.response_templates.help_template import HelpResponseTemplate
from sms.throttlers import ChatMinuteThrottle, ChatHourThrottle, ChatDayThrottle

logger = logging.getLogger(__name__)


class SMSWebsiteView(APIView):

    FAILED = "Unable to resolve your request. Please try another, such as 'food at 222 Main St'."

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ChatMinuteThrottle, ChatHourThrottle, ChatDayThrottle]

    def post(self, request: Request, *args, **kwargs):
        http_status = status.HTTP_400_BAD_REQUEST
        deserializer = WebSMSSerializer(data=request.data)
        if deserializer.is_valid():
            try:
                response = SMSService.process_web_sms(
                    msg=deserializer.validated_data["query"],
                    session=request._request.session,
                )
            except Exception as e:
                http_status = status.HTTP_404_NOT_FOUND
            else:
                http_status = status.HTTP_200_OK
                return Response({"success": True, "data": response}, status=http_status)
        else:
            msg = f"Deserialization failed for deserializer `{deserializer.__class__.__name__}`. Errors: {deserializer.errors}"
            logger.error(msg)
        return Response({"success": False, "data": self.FAILED}, status=http_status)



class SMSWebhookView(APIView):

    authentication_classes = [TwilioSignatureAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [FormParser, JSONParser]

    @staticmethod
    def to_twiml(msg: str) -> str:
        """
        Converts the response text to TwiML, a type of XML that Twilio Gateway requires.
        """
        mr = MessagingResponse()
        mr.message(msg)
        logger.info("Created TwiML response")
        return str(mr)


    def post(self, request:Request, *args, **kwargs):

        response = None
        try:
            deserializer = TwilioSMSSerializer(data=request.data)
            if deserializer.is_valid():
                response = SMSService.process_sms(
                    msg=deserializer.validated_data["Body"],
                    phone_number=deserializer.validated_data["From"],
                    message_sid=deserializer.validated_data["MessageSid"],
                )
            else:
                logger.error(f"Failed to deserialize: {deserializer.errors}")
        except Exception as e:
            msg = f"Error `{e.__class__.__name__}` caught by high-level try/except in SMSWebhookView. Details: {e}"
            logger.error(msg, exc_info=True)
            if settings.DEBUG == True:
                logger.warning("Error is being raised due to DEBUG = True in settings.py. Disable this in production and error will not be raised!")
                raise
        
        if response is None:
            twiml = self.to_twiml(msg=HelpResponseTemplate.help_msg())
        else:
            twiml = self.to_twiml(msg=response)

        return HttpResponse(twiml, content_type="text/xml", status=status.HTTP_200_OK)
    

