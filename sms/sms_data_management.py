import logging
from typing import Type
from django.contrib.gis.geos import Point
from django.db import transaction
from sms.abstract_models import IncomingSMSMessageModel
from sms.models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry, Conversation
from sms.resolvers import ResolvedSMS
from sms.resolvers.enums import ResolvedSMSType


logger = logging.getLogger(__name__)


class SMSDataManager:
    
    def __init__(self, sms_data: ResolvedSMS, location: Point|None = None):
        self.sms_data = sms_data
        self.location = location
        self.conversation = self._conversation(sms_data.phone_number)

    def _conversation(self, phone_number: str) -> Conversation:
        return Conversation.objects.get_or_create_conversation(phone_number)

    def _save_inquiry_sms(self) -> SMSInquiry:
        return SMSInquiry.objects.save_inquiry_sms(
            conversation=self.conversation,
            location=self.location,
            sms_data=self.sms_data.data,
        )

    def _save_follow_up_sms(self) -> SMSFollowUpInquiry:
        return SMSFollowUpInquiry.objects.save_follow_up_sms(
            conversation=self.conversation,
            sms_data=self.sms_data.data,
        )

    def _save_unresolved_sms(self) -> UnresolvedSMSInquiry:
        return UnresolvedSMSInquiry.objects.save_unresolved_sms(
            conversation=self.conversation,
            message=self.sms_data.data.msg,
        )


    def save_sms(self):
        """Main flow-control method to save SMS to the correct table."""
        with transaction.atomic():
            if self.sms_data.resolved_sms_type == ResolvedSMSType.INQUIRY:
                return self._save_inquiry_sms()
            elif self.sms_data.resolved_sms_type == ResolvedSMSType.FOLLOW_UP:
                return self._save_follow_up_sms()
            elif self.sms_data.resolved_sms_type == ResolvedSMSType.UNRESOLVED:
                return self._save_unresolved_sms()
            else:
                msg = f"Invalid ResolvedSMSType enum: `{self.sms_data.resolved_sms_type}`"
                logger.error(msg)
                raise TypeError(msg)