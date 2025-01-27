import json
import logging
from django.core.cache import cache, caches
from django.core.cache.backends.base import BaseCache
from typing import Any, Callable
from .enums import RedisKeyEnum, RedisStoreEnum
from .exc import RedisClientException
from .access_patterns import *

logger = logging.getLogger(__name__)


class RedisClient:

    @staticmethod
    def _redis_store(redis_store_enum:RedisKeyEnum) -> BaseCache:
        try:
            return caches[redis_store_enum.value]
        except KeyError as e:
            logger.error(f"Invalid Redis store: `{redis_store_enum}`. Available stores: {list(caches)}", exc_info=True)
            raise RedisClientException(f"Invalid Redis store: `{redis_store_enum}`") from e
        
    @staticmethod
    def _get_cached_data(redis_store:BaseCache, redis_key:RedisKeyEnum) -> Any | None:
        try:
            cached_data = redis_store.get(redis_key.value)
            if cached_data:
                logger.debug(f"Cache hit for key: {redis_key}")
                return json.loads(cached_data) if isinstance(cached_data, str) else cached_data
        except Exception as e:
            logger.error(f"Error fetching key `{redis_key}` from Redis: {e}", exc_info=True)


    @classmethod
    def get_or_set_kv(
            cls, 
            access_pattern: AccessPatternKV,
    ) -> Any:
        """
        Fetch from Redis if available; otherwise, set a value if provided.

        Args:
            redis_key (str): Redis key as a string.
            redis_store_enum (RedisStoreEnum): The Redis "store" to use.
            value (Any): Value to set if key is missing.
            ttl (int): Time-to-live for Redis key in seconds.

        Returns:
            Any: Data from Redis or the newly set value.
        """
        redis_store = cls._redis_store(access_pattern.redis_store_enum)
        cached_data = cls._get_cached_data(
            redis_store=redis_store, 
            redis_key=access_pattern.redis_key_enum
        )
        if cached_data is not None:
            return cached_data

        # If value is provided, set it in Redis
        if access_pattern.value is not None:
            try:
                serialized_value = json.dumps(access_pattern.value) if isinstance(access_pattern.value, (dict, list)) else access_pattern.value
                redis_store.set(
                    key=access_pattern.redis_key_enum.value, 
                    value=serialized_value, 
                    timeout=access_pattern.key_ttl_enum.value
                )
                logger.debug(f"Key `{access_pattern.redis_key_enum}` set in Redis with TTL=`{access_pattern.key_ttl_enum}`")
                return access_pattern.value
            except Exception as e:
                logger.error(f"Error setting key `{access_pattern.redis_key_enum}` in Redis: {e}", exc_info=True)
                raise RedisClientException("Failed to set key in Redis.") from e

        return None

    @classmethod
    def get_or_set_db(
        cls,
        access_pattern: AccessPatternDB,
        query_params: dict = None,
    ) -> Any:
        """
        Fetch from Redis if available; otherwise, query the DB, cache the result, and return it.
        """
        redis_store = cls._redis_store(access_pattern.redis_store_enum)
        cached_data = cls._get_cached_data(
            redis_store=redis_store,
            redis_key=access_pattern.redis_key_enum
        )
        if cached_data is not None:
            return cached_data
        # Cache miss, fetch from DB
        try:
            logger.debug(f"Cache miss for key: `{access_pattern.redis_key_enum}`. Fetching from DB...")
            db_data = access_pattern.query(**(query_params or {}))
            serialized_data = json.dumps(db_data)
            cache.set(access_pattern.redis_key_enum.value, serialized_data, access_pattern.key_ttl_enum.value)
            logger.debug(f"Key `{access_pattern.redis_key_enum}` updated in Redis with TTL=`{access_pattern.key_ttl_enum}`")
            return db_data
        except Exception as e:
            logger.error(f"Error fetching data for key `{access_pattern.redis_key_enum}` from DB: {e}", exc_info=True)
            raise


@staticmethod
def clear_key(redis_key_enum: RedisKeyEnum) -> None:
    try:
        cache.delete(redis_key_enum.value)
        logger.info(f"Key `{redis_key_enum}` cleared from Redis.")
    except Exception as e:
        logger.error(f"Error clearing key `{redis_key_enum}` from Redis: {e}", exc_info=True)