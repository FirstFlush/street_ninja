from datetime import datetime, timezone
import logging
from django.contrib.gis.geos import Point
from django.db import transaction
from common.utils import now
from geo.models import Location
from sms.abstract_models import IncomingSMSMessageModel
from sms.models import (
    SMSInquiry, 
    SMSFollowUpInquiry, 
    UnresolvedSMSInquiry, 
    Conversation,
    PhoneNumber,
    SMSInquiryResponse,
    SMSFollowUpResponse,
    # SMSUnresolvedResponse
)
from sms.response.response_service import SMSInquiryResponseData, SMSFollowUpResponseData
from sms.resolvers.dataclasses import ResolvedSMS
from sms.enums import ResolvedSMSType, SMSFollowUpKeywordEnum


logger = logging.getLogger(__name__)


class PersistenceService:

    def __init__(self, sms_data: ResolvedSMS, inquiry_location: Location | None = None):
        self.sms_data = sms_data
        self.sms_data.data.msg = self.sms_data.data.msg[:256]   # truncate to 256 for DB
        self.inquiry_location = inquiry_location
        self.now = now()
        logger.info(f"{self.__class__.__name__}.now stringified: `{self.now.strftime('%Y-%m-%d %H:%M:%S')}`")
        self.phone_number = self._phone_number(sms_data.phone_number)
        conversation, created = self._conversation()
        self.conversation = conversation
        self.new_session = created
        self.instance : None | SMSInquiry | SMSFollowUpInquiry | UnresolvedSMSInquiry = None

    def _phone_number(self, phone_number: str) -> PhoneNumber:
        phone, created = PhoneNumber.objects.get_or_create(number=phone_number, defaults={"last_active": self.now})
        logger.info(f"PhoneNumber `{phone.id}` found. Created: `{created}`")
        return phone

    def _conversation(self) -> tuple[Conversation, bool]:
        convo, created =  Conversation.objects.get_or_create_conversation(phone_number=self.phone_number, now=self.now)
        if created:
            logger.info(f"new Conversation with id `{convo.id}` created")
        else:
            logger.info(f"found active Conversation with id `{convo.id}`")
        return convo, created

    def _save_inquiry_sms(self) -> SMSInquiry:
        return SMSInquiry.objects.save_inquiry_sms(
            conversation=self.conversation,
            sms_data=self.sms_data.data,
            inquiry_location=self.inquiry_location,
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


    def save_inquiry_response(self, response_data: SMSInquiryResponseData) -> SMSInquiryResponse:
        try:
            response = SMSInquiryResponse.objects.create(
                sms_inquiry=self.instance,
                conversation=self.instance.conversation,
                resource_ids=response_data.ids,
            )
        except Exception as e:
            msg = f"Error while trying to create SMSInquiryResponse for `{self.instance.__class__.__name__}` #`{self.instance.id}`: {e}"
            logger.error(msg, exc_info=True)
            raise
        else:
            logger.info(f"Create SMSInquiryResponse id `{response.id}`")
            return response
        

    def save_follow_up_response(self, response_data: SMSFollowUpResponseData) -> SMSFollowUpResponse:
        params = {
            'sms_follow_up': self.instance,
            'conversation': self.instance.conversation,
            'resource_ids': response_data.ids,
        }
        match self.instance.keyword_enum:
            case SMSFollowUpKeywordEnum.DIRECTIONS:
                params = params | {'directions': response_data.msg}
            case _:
                pass
        try:
            response = SMSFollowUpResponse.objects.create(**params)
        except Exception as e:
            msg = f"Error while trying to create SMSFollowUpResponse for `{self.instance.__class__.__name__}` #`{self.instance.id}`: {e}"
            logger.error(msg, exc_info=True)
            raise
        else:
            logger.info(f"Created SMSFollowUpResponse id `{response.id}`")
            return response
