import logging
from common.utils import now
from sms.models import SMSFollowUpInquiry
from .base_cache_service import BaseCacheService
from .dataclasses import PhoneSessionData
from .redis.exc import NoSessionFound
from .redis.access_patterns.pattern_registry import AccessPatternRegistry


logger = logging.getLogger(__name__)


class FollowUpCachingService(BaseCacheService):

    @classmethod
    def init(cls, follow_up_inquiry: SMSFollowUpInquiry) -> tuple["FollowUpCachingService", PhoneSessionData]:
        session_cache_client = cls._get_session_cache_client(convo_id=follow_up_inquiry.conversation.id)
        current_session = session_cache_client.get_session()
        if current_session is None:
            msg = f"No session object found by FollowUpCachingService for SMSFollowUpInquiry ID: `{follow_up_inquiry.id}`, Conversation ID: `{follow_up_inquiry.conversation.id}`"
            logger.warning(msg)
            raise NoSessionFound(msg)
        
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
            ids: list[int] | None = None,
    ) -> PhoneSessionData:
        """
        Updates session when a 'MORE' request comes in by adding the IDs onto the list.
        For 'INFO' and 'DIRECTIONS' it just updates the timestamp.
        """
        if ids is not None:
            session_data.ids.extend(ids)
        session_data.last_updated = now()
        self._set_phone_session(session_data=session_data)
        return session_data  

