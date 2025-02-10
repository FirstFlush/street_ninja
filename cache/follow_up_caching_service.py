import logging
from common.utils import now
from sms.enums import SMSFollowUpKeywordEnum, SMSKeywordEnum
from sms.models import SMSFollowUpInquiry
from .base_cache_service import BaseCacheService
from .redis.clients.phone_session_client import PhoneSessionCacheClient
from .dataclasses import PhoneSessionData
from .redis.access_patterns import AccessPatternDB, PhoneSessionAccessPattern, AccessPatternRegistry


logger = logging.getLogger(__name__)


class FollowUpCachingService(BaseCacheService):

    @classmethod
    def init(cls, follow_up_inquiry: SMSFollowUpInquiry) -> tuple["FollowUpCachingService", PhoneSessionData]:
        session_cache_client = cls._get_session_cache_client(convo_id=follow_up_inquiry.conversation.id)
        current_session = session_cache_client.get_session()
        if current_session is None:
            msg = f"No session object found by FollowUpCachingService for SMSFollowUpInquiry ID `{follow_up_inquiry.id}`!"
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Initialized PhoneSessionCacheClient")
        resource_access_pattern = AccessPatternRegistry.get_pattern(
           sms_keyword_enum=current_session.keyword_enum
        )
        logger.info(f"Resource Access pattern `{resource_access_pattern.__name__}` loaded for SMSFollowUpInquiry ID `{follow_up_inquiry.id}`")
        return cls(
            inquiry=follow_up_inquiry,
            resource_access_pattern=resource_access_pattern,
            session_cache_client = session_cache_client,
        ), current_session


    def update_phone_session(
            self, 
            session_data: PhoneSessionData,
            ids: list[int],
    ) -> PhoneSessionData:
        session_data.ids = ids
        session_data.last_updated = now()
        self._set_phone_session(session_data=session_data)
        return session_data

    def directions(self):
        ...

    def info(self):
        ...

    def more(self):
        ...