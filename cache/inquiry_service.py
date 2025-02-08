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
    def process_inquiry(cls, inquiry: SMSInquiry) -> "InquiryCachingService":
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
        session_data = inquiry_service.get_phone_session()
        if session_data is None:
            inquiry_service.set_phone_session(session_data=inquiry_service._create_phone_session_data())
