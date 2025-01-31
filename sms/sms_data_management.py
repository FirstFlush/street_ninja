from sms.models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry, Conversation
from sms.resolvers import ResolvedSMS


class SMSDataManager:
    
    def __init__(self, sms_data: ResolvedSMS):
        self.sms_data = sms_data
