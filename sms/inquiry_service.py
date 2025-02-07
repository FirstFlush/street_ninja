import logging
from .models import SMSInquiry
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


logger = logging.getLogger(__name__)


class InquiryProcessingService:

    def __init__(self, inquiry: SMSInquiry, resource_access_pattern: AccessPatternDB):
        self.inquiry = inquiry
        self.resource_access_pattern = resource_access_pattern

    @classmethod
    def process_inquiry(cls, inquiry: SMSInquiry) -> "InquiryProcessingService":
        """
        Factory method for selecting instantiating InquiryProcessingService 
        with the inquiry's appropriate access pattern.
        #NOTE change this name since SMSResponseService will be running at the same time
        """
        resource_access_pattern = AccessPatternRegistry.get_resource(
           sms_keyword_enum=inquiry.keyword_enum
        )
        logger.info(f"Resource Access pattern `{resource_access_pattern.__class__.__name__}` loaded for SMSInquiry ID `{inquiry.id}`")
        inquiry_service = cls(
            inquiry=inquiry, 
            resource_access_pattern=resource_access_pattern,
        )
        inquiry_service._get_resources()


    # def _set_phone_session(self):

    #     last_updated = self.inquiry.conversation.last_updated.isoformat()

        # PhoneSessionData(
        #     keyword=SMSInquiry.keyword,
        #     order=None,
        #     offset=0,
        #     last_updated=last_updated,
        # )


    def _get_resources(self):
        inquiry_params = self.inquiry.params or {}
        client = ResourceCacheClient(access_pattern=self.resource_access_pattern)
        return client.get_or_set_db(query_params=inquiry_params).closest_to(self.inquiry.location)
