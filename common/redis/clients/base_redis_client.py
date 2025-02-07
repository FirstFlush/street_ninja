from abc import ABC
import json
import logging
from django.core.cache import cache, caches
from django.core.cache.backends.base import BaseCache
from typing import Any, Type
from ..enums import RedisStoreEnum, RedisKeyEnum
from ..exc import RedisClientException, InvalidAccessPattern
from ..access_patterns import *
from ..access_patterns.base_access_patterns import BaseRedisAccessPattern


logger = logging.getLogger(__name__)


class BaseRedisClient(ABC):

    def __init__(self, access_pattern:BaseRedisAccessPattern):
        self.access_pattern = access_pattern
        self.redis_store_enum: None | RedisStoreEnum = None
        self.redis_store: None | BaseCache = None
        # self.redis_store = self._redis_store()


    def _redis_store(self) -> BaseCache:
        try:
            return caches[self.__class__.redis_store_enum.value]
        except KeyError as e:
            logger.error(
                f"Invalid Redis store: `{self.redis_store_enum}`. Available stores: {list(caches)}",
                exc_info=True
            )
            raise RedisClientException(f"Invalid Redis store: `{self.redis_store_enum}`") from e


    def _get_cached_data(self, redis_key: RedisKeyEnum, raise_error: bool= False) -> Any | None:
        """
        Retrieve cached data from Redis.

        Args:
            redis_store (BaseCache): The Redis store to query.
            redis_key (RedisKeyEnum): The Redis key to fetch.

        Returns:
            Any | None: Cached data if available, otherwise None.

        Logs:
            - Cache hit or miss.
            - Errors when fetching data from Redis.
        """
        try:
            cached_data = self.redis_store.get(redis_key.value)
            if cached_data:
                logger.debug(f"Cache hit for key: {redis_key}")
                return json.loads(cached_data) if isinstance(cached_data, str) else cached_data
        except Exception as e:
            if raise_error:
                logger.error(f"Error fetching key `{redis_key}` from Redis: {e}", exc_info=True)
                raise
        return None


    def _validate_access_pattern_type(self, expected_type:Type["BaseRedisAccessPattern"]):

        if not isinstance(self.access_pattern, expected_type):
            error_msg = f"Access pattern must be of type AccessPatternDB, not `{type(self.access_pattern).__name__}`"
            logger.error(error_msg)
            raise RedisClientException("RedisClient failed due to an invalid access pattern.") from InvalidAccessPattern(error_msg)


    @staticmethod
    def clear_key(redis_key_enum: RedisKeyEnum) -> None:
        """
        Clear a specific key from Redis.

        Args:
            redis_key_enum (RedisKeyEnum): The Redis key to clear.

        Logs:
            - Success or failure in clearing the key.
        """
        try:
            cache.delete(redis_key_enum.value)
            logger.debug(f"Key `{redis_key_enum}` cleared from Redis.")
        except Exception as e:
            logger.error(f"Error clearing key `{redis_key_enum}` from Redis: {e}", exc_info=True)


