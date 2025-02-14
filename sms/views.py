import logging
from django.conf import settings
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Request, Response, status
from twilio.twiml.messaging_response import MessagingResponse
from auth.authentication import TwilioSignatureAuthentication
from .serializers import TwilioSMSSerializer
from .sms_service import SMSService
from sms.response.response_templates.help_template import HelpResponseTemplate


logger = logging.getLogger(__name__)


class SMSWebhookView(APIView):

    # authentication_classes = [TwilioSignatureAuthentication]
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
                raise
        
        if response is None:
            twiml = self.to_twiml(msg=HelpResponseTemplate.help_msg())
        else:
            twiml = self.to_twiml(msg=response)

        return Response(twiml, content_type="application/xml", status=status.HTTP_200_OK)
    




        # deserializer = TwilioSMSSerializer(data=request.data)
        # if deserializer.is_valid():
        #     SMSService.process_sms(
        #         msg=deserializer.validated_data["Body"],
        #         phone_number=deserializer.validated_data["From"],
        #         message_sid=deserializer.validated_data["MessageSid"],
        #     )
        # else:
        #     logger.error(f"Failed to deserialize: {deserializer.errors}")
        #     return Response("Could not parse message", status=status.HTTP_400_BAD_REQUEST)

        # return Response("fasdfasd", status=status.HTTP_200_OK)
    
