from datetime import datetime, timezone
import logging
from abc import ABC, abstractmethod
from django.conf import settings
from cache.dataclasses import PhoneSessionData
from cache.redis.clients import ResourceCacheClient, PhoneSessionCacheClient
from resources.abstract_models import ResourceQuerySet
from sms.models import SMSFollowUpInquiry, SMSInquiry
from .redis.access_patterns import AccessPatternDB, PhoneSessionAccessPattern


logger = logging.getLogger(__name__)


class BaseCacheService(ABC):

    def __init__(
            self, 
            inquiry: SMSInquiry, 
            resource_access_pattern: AccessPatternDB,
            session_access_pattern: PhoneSessionAccessPattern = PhoneSessionAccessPattern
    ):
        self.inquiry = inquiry
        self.resource_access_pattern = resource_access_pattern
        self.session_access_pattern = session_access_pattern
        self.resource_cache_client = ResourceCacheClient(access_pattern=self.resource_access_pattern)
        self.session_cache_client = PhoneSessionCacheClient(
            redis_key=self._get_redis_key(), 
            access_pattern=self.session_access_pattern,
        )

    # def _create_phone_session_data(
    #         self, 
    #         ids: list[int],
    #         last_updated: datetime, 
    #         offset: int, 
    # ) -> PhoneSessionData:
    #     """Creates the default data for phone session"""
    #     return PhoneSessionData(
    #         keyword=self.inquiry.keyword,
    #         ids=ids,
    #         offset=offset,
    #         last_updated=last_updated,
        # )

    @staticmethod
    def _now() -> datetime:
        return datetime.now(tz=timezone.utc)


    def _get_redis_key(self) -> str:
        try:
            return f"{self.session_access_pattern.redis_key_format}{self.inquiry.conversation.id}"
        except AttributeError as e:
            logger.error(e, exc_info=True)
            raise

    def get_resources_by_proximity(self) -> ResourceQuerySet:
        inquiry_params = self.inquiry.params or {}
        return self.resource_cache_client.get_or_set_db(query_params=inquiry_params).closest_to(self.inquiry.location)

    def get_phone_session(self) -> PhoneSessionData | None:
        return self.session_cache_client.get_session()

    def _set_phone_session(self, session_data: PhoneSessionData) -> PhoneSessionData:
        """Returns session_data just to be consistent with get_phone_session() flow."""
        return self.session_cache_client.set_session(session_data=session_data)
