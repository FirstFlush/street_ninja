import logging
from sms.enums import SMSFollowUpKeywordEnum
from sms.models import SMSFollowUpInquiry
from .base_cache_service import BaseCacheService
from .dataclasses import PhoneSessionData
from .redis.access_patterns import AccessPatternDB, PhoneSessionAccessPattern


logger = logging.getLogger(__name__)


class FollowUpCachingService(BaseCacheService):

    def get_phone_session(self) -> PhoneSessionData:
        session_data = self.session_cache_client.get_session()
        if session_data is None:
            msg = "session is None on follow-up request!"
            logger.error(msg)
            raise Exception(msg)