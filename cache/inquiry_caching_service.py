
import logging
from typing import Any
from .base_cache_service import BaseCacheService
from .dataclasses import PhoneSessionData
from .redis.access_patterns.pattern_registry import AccessPatternRegistry
from common.utils import now
from sms.models import SMSInquiry


logger = logging.getLogger(__name__)


class InquiryCachingService(BaseCacheService):


    def create_phone_session(
            self, 
            ids: list[int], 
            params: dict[str, Any] | None = None
    ) -> PhoneSessionData:
        session_data = PhoneSessionData(
            last_updated=now(),
            inquiry_id=self.inquiry.id,
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
        """
        Updates session when an sms inquiry comes in.
        This is differet from create session, as one session can have multiple inquiries.
        """
        session_data.ids = ids
        session_data.keyword = self.inquiry.keyword
        session_data.inquiry_id = self.inquiry.id
        session_data.last_updated = now()
        self._set_phone_session(session_data=session_data)
        return session_data 
    

    @classmethod
    def init(cls, inquiry: SMSInquiry) -> "InquiryCachingService":
        """
        Factory method for selecting instantiating InquiryProcessingService 
        with the inquiry's appropriate access pattern.
        """
        session_cache_client = cls._get_session_cache_client(convo_id=inquiry.conversation.id)
        logger.info("Initialized PhoneSessionCacheClient")
        resource_access_pattern = AccessPatternRegistry.get_pattern(
           sms_keyword_enum=inquiry.keyword_enum
        )
        logger.info(f"Resource Access pattern `{resource_access_pattern.__name__}` loaded for SMSInquiry ID `{inquiry.id}`")
        return cls(
            inquiry=inquiry,
            resource_access_pattern=resource_access_pattern,
            session_cache_client = session_cache_client
        )