from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS, 
)
from sms.resolvers.exc import SMSResolutionError
from sms.serializers import TwilioSMSSerializer

class SMSService:

    def __init__(self, msg: str, phone_number: str, message_sid: str):

        self.resolver = SMSResolver(msg=msg)
        self.sms_data = self.resolver.resolve_sms(
            message_sid=message_sid,
            phone_number=phone_number,
        )
