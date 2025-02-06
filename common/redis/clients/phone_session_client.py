import logging
from typing import Type
from .base_redis_client import BaseRedisClient
from ..enums import RedisStoreEnum
from ..access_patterns import PhoneSessionAccessPattern


logger = logging.getLogger(__name__)


class PhoneSessionCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.PHONE_SESSION

    def __init__(
            self, 
            phone_number: str, 
            access_pattern: Type[PhoneSessionAccessPattern] = Type[PhoneSessionAccessPattern]
    ):
        super().__init__(
            phone_number=phone_number,
            access_pattern=access_pattern,
        )
        self.phone_number = phone_number
        self._validate_access_pattern_type(expected_type=PhoneSessionAccessPattern)
        self.redis_store = self._redis_store()
        self.redis_key = self._get_redis_key()
        self.access_pattern:PhoneSessionAccessPattern


    def _get_redis_key(self):
        try:
            return self.access_pattern.redis_key_format.format(self.phone_number)
        except AttributeError as e:
            logger.error(e, exc_info=True)
            raise


    def get_session(self) -> dict:
        phone_session_data = self._get_cached_data(redis_key=self.redis_key)
        if not isinstance(phone_session_data, dict):
            msg = f"Wrong type `{type(phone_session_data)}` for cached_data: {phone_session_data} using redis key: `{self.redis_key}`"
            logger.error(msg)
            raise TypeError(msg)
        return phone_session_data

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