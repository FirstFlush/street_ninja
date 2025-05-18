from dataclasses import asdict
from datetime import datetime
import json
import logging
from typing import Any, Type
from .base_redis_client import BaseRedisClient
from cache.dataclasses import PhoneSessionData
from ..enums import RedisStoreEnum
from ..access_patterns.phone_session import PhoneSessionAccessPattern


logger = logging.getLogger(__name__)


class PhoneSessionCacheClient(BaseRedisClient):

    def __init__(
            self,
            redis_key: str,
            access_pattern: Type[PhoneSessionAccessPattern] = PhoneSessionAccessPattern
    ):
        super().__init__(access_pattern=access_pattern)
        self.redis_key = redis_key
        self.redis_store = self._redis_store()
        self.access_pattern: Type[PhoneSessionAccessPattern]


    @staticmethod
    def get_redis_key(convo_id:int, phone_session_access_pattern:PhoneSessionAccessPattern) -> str:
        try:
            return f"{phone_session_access_pattern.redis_key_format}{convo_id}"
        except AttributeError as e:
            logger.error(e, exc_info=True)
            raise


    def get_session(self) -> PhoneSessionData | None:
        cached_data = self._get_cached_data(redis_key=self.redis_key, raise_error=True)
        if cached_data is not None:
            phone_session = self._build_phone_session_from_cache(cached_data)
            logger.info(f"phone session retrieved for redis key `{self.redis_key}`")
            return phone_session

        logger.warning(f"phone session not found for redis key `{self.redis_key}`")
        return None

    def _build_phone_session_from_cache(self, cached_data: dict[str, Any]) -> PhoneSessionData:
        cached_data["last_updated"] = datetime.fromisoformat(cached_data["last_updated"])
        return PhoneSessionData(**cached_data)

    def set_session(self, session_data: PhoneSessionData) -> PhoneSessionData:
        session_dict = asdict(session_data)
        session_dict["last_updated"] = session_data.last_updated.isoformat()
        try:
            value = json.dumps(session_dict)
            self.redis_store.set(
                key=self.redis_key, 
                value=value, 
                timeout=self.access_pattern.key_ttl_enum.value
            )
            logger.info(f"phone session set for Redis key `{self.redis_key}`")
        except Exception as e:
            logger.error(f"Failed to set session for Redis key `{self.redis_key}`: {e}", exc_info=True)
            raise 

        return session_data
    
