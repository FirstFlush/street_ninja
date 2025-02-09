from datetime import datetime
import logging
from .base_cache_service import BaseCacheService
from .dataclasses import PhoneSessionData
from .redis.access_patterns.base_access_patterns import AccessPatternDB
from .redis.access_patterns.phone_session import PhoneSessionAccessPattern
from .redis.access_patterns.pattern_registry import AccessPatternRegistry
from .redis.clients.resource_client import ResourceCacheClient
from .redis.clients.phone_session_client import PhoneSessionCacheClient
from resources.abstract_models import ResourceQuerySet
from sms.models import SMSInquiry


logger = logging.getLogger(__name__)


class InquiryCachingService(BaseCacheService):


    @classmethod
    def init(cls, inquiry: SMSInquiry) -> "InquiryCachingService":
        """
        Factory method for selecting instantiating InquiryProcessingService 
        with the inquiry's appropriate access pattern.
        """
        resource_access_pattern = AccessPatternRegistry.get_pattern(
           sms_keyword_enum=inquiry.keyword_enum
        )
        logger.info(f"Resource Access pattern `{resource_access_pattern.__name__}` loaded for SMSInquiry ID `{inquiry.id}`")
        return cls(
            inquiry=inquiry,
            resource_access_pattern=resource_access_pattern,
        )
        
        # session_data = inquiry_service.get_phone_session()
        # if session_data is None:
        #     print("no session found!")
            # inquiry_service.set_phone_session(session_data=inquiry_service._create_phone_session_data(
            #     batch_ids=...,
            #     last_updated=inquiry_service.inquiry.conversation.last_updated,
            #     offset=...,
            # ))

        # NOTE need to build Response service to get batch ids and offset. SMSService will pass it a queryset, fetched by this class,
        # and ResponseService will determine how many items fit in the response, and truncate accordingly.
        # most likely this class method will be destroyed and the flow-control will be handled by SMSService.