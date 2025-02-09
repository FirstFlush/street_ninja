import logging
from django.contrib.gis.geos import Point
from django.db import transaction
from sms.abstract_models import IncomingSMSMessageModel
from sms.models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry, Conversation
from sms.resolvers import ResolvedSMS
from sms.enums import ResolvedSMSType


logger = logging.getLogger(__name__)


class PersistenceService:
    
    def __init__(self, sms_data: ResolvedSMS, location: Point|None = None):
        self.sms_data = sms_data
        self.location = location
        self.conversation = self._conversation(sms_data.phone_number)
        self.instance : None | SMSInquiry | SMSFollowUpInquiry | UnresolvedSMSInquiry = None

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

    # def _get_resource_access_pattern(self) -> AccessPatternDB:
    #     return AccessPatternRegistry.get_resource(
    #         sms_keyword_enum=self.sms_data.data.keyword_language_data.sms_keyword_enum
    #     )


    # def fetch_resources(self) -> ResourceQuerySet[ResourceModel]:
    #     access_pattern = self._get_resource_access_pattern()
    #     qs:ResourceQuerySet = RedisClient.get_or_set_db(access_pattern=access_pattern)
    #     qs.closest_to(location=self.location)


    def save_sms(self):
        """
        Main flow-control method to save SMS to the correct table.
        Sets self.instance to the saved instance
        """
        with transaction.atomic():
            match self.sms_data.resolved_sms_type:
                case ResolvedSMSType.INQUIRY:
                    self.instance = self._save_inquiry_sms()
                case ResolvedSMSType.FOLLOW_UP:
                    self.instance = self._save_follow_up_sms()
                case ResolvedSMSType.UNRESOLVED:
                    self.instance = self._save_unresolved_sms()
                case _:
                    msg = f"Invalid ResolvedSMSType enum: `{self.sms_data.resolved_sms_type}`"
                    logger.error(msg)
                    raise TypeError(msg)
        
        logger.info(f"Saved {self.instance.__class__.__name__} instance: `{self.instance}`")


