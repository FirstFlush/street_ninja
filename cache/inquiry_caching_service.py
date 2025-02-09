from datetime import datetime, timezone
import logging
from typing import Any
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


    def create_phone_session(
            self, 
            ids: list[int], 
            params: dict[str, Any] | None = None
    ) -> PhoneSessionData:
        now = self._now()
        session_data = PhoneSessionData(
            last_updated=now,
            keyword=self.inquiry.keyword,
            ids=ids,
            resource_params=params
        )
        self._set_phone_session(session_data=session_data)
        return session_data

    def update_phone_session(
            self, 
            session_data: PhoneSessionData,
            ids: list[int],
    ) -> PhoneSessionData:
        session_data.ids = ids
        session_data.keyword = self.inquiry.keyword
        session_data.last_updated = self._now()
        self._set_phone_session(session_data=session_data)
        return session_data



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
            #     ids=...,
            #     last_updated=inquiry_service.inquiry.conversation.last_updated,
            #     offset=...,
            # ))

        # NOTE need to build Response service to get batch ids and offset. SMSService will pass it a queryset, fetched by this class,
        # and ResponseService will determine how many items fit in the response, and truncate accordingly.