from dataclasses import asdict
from datetime import datetime
import json
import logging
from typing import Any, Type
from sms.models import SMSInquiry, Conversation
from .base_redis_client import BaseRedisClient
from ..dataclasses import PhoneSessionData
from ..enums import RedisStoreEnum
from ..access_patterns import PhoneSessionAccessPattern


logger = logging.getLogger(__name__)


class PhoneSessionCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.PHONE_SESSION

    def __init__(
            self,
            inquiry: SMSInquiry,
            access_pattern: Type[PhoneSessionAccessPattern] = PhoneSessionAccessPattern
    ):
        super().__init__(access_pattern=access_pattern)
        self.inquiry = inquiry
        # self._validate_access_pattern_type(expected_type=PhoneSessionAccessPattern)
        self.redis_store = self._redis_store()
        self.redis_key = self._get_redis_key()
        self.access_pattern: Type[PhoneSessionAccessPattern]

    def _get_redis_key(self):
        try:
            return f"{self.access_pattern.redis_key_format}{self.inquiry.conversation.id}"
        except AttributeError as e:
            logger.error(e, exc_info=True)
            raise

    def get_session(self) -> PhoneSessionData:
        cached_data = self._get_cached_data(redis_key=self.redis_key)
        if cached_data is None:
            logger.warning(f"phone session not found for conversation id `{self.inquiry.conversation.id}`")
            phone_session = self._set_session()
        else:
            phone_session = self._build_session_data(cached_data)
            logger.info(f"phone session retrieved for conversation id `{self.inquiry.conversation.id}`")
        return phone_session

    def _build_session_data(self, cached_data: dict[str, Any]) -> PhoneSessionData:
        cached_data["last_updated"] = datetime.fromisoformat(cached_data["last_updated"])
        return PhoneSessionData(**cached_data)

    def _default_session_data(self) -> PhoneSessionData:
        return PhoneSessionData(
            last_updated=self.inquiry.conversation.last_updated,
            keyword=self.inquiry.keyword,
            order=None,
            offset=0,
        )

    def _set_session(self) -> PhoneSessionData:
        session_data = self._default_session_data()
        session_dict = asdict(session_data)
        session_dict["last_updated"] = session_data.last_updated.isoformat()
        try:
            value = json.dumps(session_dict)
            self.redis_store.set(key=self.redis_key, value=value, timeout=self.access_pattern.key_ttl_enum.value)
            logger.info(f"phone session set for {self.redis_key}")
        except Exception as e:
            logger.error(f"Failed to set session in Redis for key `{self.redis_key}`: {e}", exc_info=True)
            raise 

        return session_data
    

    # @classmethod
    # def get_or_set_phone_session(
    #         cls, 
    #         phone_number:str, 
    #         access_pattern:PhoneSessionAccessPattern=PhoneSessionAccessPattern,
    # ) -> Any:

    #     # redis_store = cls._redis_store(access_pattern.redis_store_enum)
    #     redis_key = cls._get_redis_key(
    #         phone_number=phone_number, 
    #         access_pattern=access_pattern
    #     )
    #     cached_data = cls._get_cached_data(redis_store=redis_store, redis_key=redis_key)
    #     if not isinstance(cached_data, dict):
    #         msg = f"Wrong type `{type(cached_data)}` for cached_data: {cached_data} using redis key: `{redis_key}`"
    #         logger.error(msg)
    #         raise TypeError(msg)


        # if cached_data is not None:
        #     return cached_data

        # # If value is provided, set it in Redis
        # if access_pattern.value is not None:
        #     try:
        #         serialized_value = (
        #             json.dumps(access_pattern.value)
        #             if isinstance(access_pattern.value, (dict, list))
        #             else access_pattern.value
        #         )
        #         redis_store.set(
        #             key=access_pattern.redis_key_enum.value,
        #             value=serialized_value,
        #             timeout=access_pattern.key_ttl_enum.value,
        #         )
        #         logger.debug(
        #             f"Key `{access_pattern.redis_key_enum}` set in Redis with TTL=`{access_pattern.key_ttl_enum}`"
        #         )
        #         return access_pattern.value
        #     except Exception as e:
        #         logger.error(
        #             f"Error setting key `{access_pattern.redis_key_enum}` in Redis: {e}",
        #             exc_info=True,
        #         )
        #         raise RedisClientException("Failed to set key in Redis.") from e

        # return None