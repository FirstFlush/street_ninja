import logging
import random
from django.contrib.sessions.backends.base import SessionBase
from .base_redis_client import BaseRedisClient
from ..enums import RedisStoreEnum
from ..access_patterns.web_session import WebSessionAccessPattern


logger = logging.getLogger(__name__)


class WebSessionCacheClient(BaseRedisClient):

    def __init__(
            self, 
            access_pattern: WebSessionAccessPattern,
            session: SessionBase
    ):
        self.access_pattern = access_pattern
        self.session = session

    @staticmethod
    def _create_phone_number() -> str:
        return f"web-{''.join(str(random.randint(0, 9)) for _ in range(16))}"

    def get_or_set_phone_number(self) -> str:
        """
        Retrieves the phone number from session cache, or generates and stores a new one.
        """
        if self.session.session_key is None:
            self.session.save()
        try:
            phone_number = self.session.get(self.access_pattern.redis_key_enum.value)
        except Exception as e:
            logger.error(f"Unexpected `{e.__class__.__name__}` error on session.get() call: {e}", exc_info=True)
            phone_number = None

        if phone_number:
            logger.info(f"Found phone number `{phone_number}` in web session")
            return phone_number
        else:
            logger.info(f"Cache miss! Creating new phone number for web session")
            phone_number = self._create_phone_number()
            try:
                self.session[self.access_pattern.redis_key_enum.value] = phone_number
                self.session.save()
            except Exception as e:
                msg = f"Unexpected `{e.__class__.__name__}` error while saving phone number `{phone_number}` to web session: {e}"
                logger.error(msg, exc_info=True)
            logger.info(f"New web phone number created: `{phone_number}`")
            return phone_number 
