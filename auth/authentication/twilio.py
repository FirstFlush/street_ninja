import hmac
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import Request
from twilio.request_validator import RequestValidator


class TwilioSignatureAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):

        twilio_signature = request._request.headers.get("X-Twilio-Signature")
        if not twilio_signature:
            raise AuthenticationFailed("Missing SMS gateway signature")

        auth_token = settings.TWILIO_AUTH_TOKEN

        # If using ngrok you may need to replace 'http' for 'https'
        # DO NOT REPLACE IN PRODUCTION
        if settings.DEBUG:
            url = request.build_absolute_uri().replace("http://", "https://") 

        post_data = request.POST.dict()
        validator = RequestValidator(auth_token)
        is_valid = validator.validate(uri=url, params=post_data, signature=twilio_signature)

        if not is_valid:
            raise AuthenticationFailed("Invalid SMS gateway")

        return (None, None)
