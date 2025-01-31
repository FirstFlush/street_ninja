from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS, 
    ResolvedKeywordAndLanguage, 
    ResolvedLocation
)
from sms.resolvers.exc import SMSResoltuionError
# from .models import Inqu


class SMSService:

    def __init__(self, resolver: SMSResolver):
        self.resolver = resolver


    def _resolve_sms(self) -> ResolvedSMS:
        try:
            resolved_sms = self.resolver.resolve_sms()
        except SMSResoltuionError:
            ...
            # create unresolved sms model