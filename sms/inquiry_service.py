import logging
from common.redis.access_patterns import (
    AccessPatternDB,
    ShelterAccessPattern,
    FoodProgramAccessPattern,
    ToiletAccessPattern,
    DrinkingFountainAccessPattern,
    PublicWifiAccessPattern,
)
from datetime import datetime, timezone
from common.redis.access_patterns import AccessPatternRegistry
from common.redis import ResourceCacheClient, PhoneSessionCacheClient, PhoneSessionData
from resources.abstract_models import ResourceQuerySet
from .models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry

logger = logging.getLogger(__name__)


class InquiryProcessingService:

    def __init__(self, inquiry: SMSInquiry, resource_access_pattern: AccessPatternDB):
        self.inquiry = inquiry
        self.resource_access_pattern = resource_access_pattern
        self.resource_cache_client = ResourceCacheClient(access_pattern=self.resource_access_pattern)
        self.session_cache_client = PhoneSessionCacheClient(inquiry=self.inquiry)


    @classmethod
    def process_inquiry(cls, inquiry: SMSInquiry) -> "InquiryProcessingService":
        """
        Factory method for selecting instantiating InquiryProcessingService 
        with the inquiry's appropriate access pattern.
        """
        resource_access_pattern = AccessPatternRegistry.get_resource(
           sms_keyword_enum=inquiry.keyword_enum
        )
        logger.info(f"Resource Access pattern `{resource_access_pattern.__name__}` loaded for SMSInquiry ID `{inquiry.id}`")
        inquiry_service = cls(
            inquiry=inquiry, 
            resource_access_pattern=resource_access_pattern,
        )



        inquiry_service.get_phone_session()




    def _get_ordered_resources(self) -> ResourceQuerySet:
        inquiry_params = self.inquiry.params or {}
        return self.resource_cache_client.get_or_set_db(query_params=inquiry_params).closest_to(self.inquiry.location)

    def _get_ordered_ids(self, qs:ResourceQuerySet) -> list[int]:
        return [instance.id for instance in qs]


    def get_phone_session(self) -> PhoneSessionData:

        session_data = self.session_cache_client.get_session()
        if session_data is None:
            session_data = self.session_cache_client.set_session(
                session_data=self._create_default_phone_session_data()
            )
        return session_data


    def _create_default_phone_session_data(self) -> PhoneSessionData:
        return PhoneSessionData(
            keyword=self.inquiry.keyword,
            order=self._get_ordered_ids(qs=self._get_ordered_resources()),
            offset=0,
            last_updated=self.inquiry.conversation.last_updated,
        )
