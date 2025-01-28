import json
import logging
from django.core.cache import cache, caches
from django.core.cache.backends.base import BaseCache
import pickle
from typing import Any
from .enums import RedisKeyEnum, RedisStoreEnum
from .exc import RedisClientException
from .access_patterns import *

logger = logging.getLogger(__name__)


class RedisClient:

    @staticmethod
    def _redis_store(redis_store_enum: RedisStoreEnum) -> BaseCache:
        """
        Retrieve the appropriate Redis store for the given Redis store enum.

        Args:
            redis_store_enum (RedisStoreEnum): The Redis store to access.

        Returns:
            BaseCache: The Redis store backend associated with the store enum.

        Raises:
            RedisClientException: If the Redis store cannot be found.
        """
        try:
            return caches[redis_store_enum.value]
        except KeyError as e:
            logger.error(
                f"Invalid Redis store: `{redis_store_enum}`. Available stores: {list(caches)}",
                exc_info=True
            )
            raise RedisClientException(f"Invalid Redis store: `{redis_store_enum}`") from e

    @staticmethod
    def _get_cached_data(redis_store: BaseCache, redis_key: RedisKeyEnum) -> Any | None:
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
            cached_data = redis_store.get(redis_key.value)
            if cached_data:
                logger.debug(f"Cache hit for key: {redis_key}")
                return json.loads(cached_data) if isinstance(cached_data, str) else cached_data
        except Exception as e:
            logger.error(f"Error fetching key `{redis_key}` from Redis: {e}", exc_info=True)
        return None

    @staticmethod
    def _pickle(data: object) -> bytes:
        try:
            return pickle.dumps(data)
        except Exception as e:
            logger.error(f"Error pickling data: {e}", exc_info=True)
            raise RedisClientException(f"Error pickling object: `{data.__class__.__name__}`") from e

    @staticmethod
    def _unpickle(data: bytes) -> object:
        try:
            return pickle.loads(data)
        except Exception as e:
            logger.error(f"Error unpickling data: {e}", exc_info=True)
            raise RedisClientException(f"Error unpickling binary data of size `{len(data)}` bytes.") from e



    @classmethod
    def get_or_set_kv(cls, access_pattern: AccessPatternKV) -> Any:
        """
        Fetch from Redis if available; otherwise, set a predefined value.

        Args:
            access_pattern (AccessPatternKV): The access pattern defining how Redis is used for this operation.

        Returns:
            Any: Data retrieved from Redis or the value that was set.

        Raises:
            RedisClientException: If setting a key in Redis fails.
        """
        redis_store = cls._redis_store(access_pattern.redis_store_enum)
        cached_data = cls._get_cached_data(redis_store=redis_store, redis_key=access_pattern.redis_key_enum)
        if cached_data is not None:
            return cached_data

        # If value is provided, set it in Redis
        if access_pattern.value is not None:
            try:
                serialized_value = (
                    json.dumps(access_pattern.value)
                    if isinstance(access_pattern.value, (dict, list))
                    else access_pattern.value
                )
                redis_store.set(
                    key=access_pattern.redis_key_enum.value,
                    value=serialized_value,
                    timeout=access_pattern.key_ttl_enum.value,
                )
                logger.debug(
                    f"Key `{access_pattern.redis_key_enum}` set in Redis with TTL=`{access_pattern.key_ttl_enum}`"
                )
                return access_pattern.value
            except Exception as e:
                logger.error(
                    f"Error setting key `{access_pattern.redis_key_enum}` in Redis: {e}",
                    exc_info=True,
                )
                raise RedisClientException("Failed to set key in Redis.") from e

        return None

    @classmethod
    def get_or_set_db(cls, access_pattern: AccessPatternDB, query_params: dict = None) -> Any:
        """
        Fetch data from Redis if available; otherwise, query the database and cache the result.

        Args:
            access_pattern (AccessPatternDB): The access pattern defining how Redis is used for this operation.
            query_params (dict, optional): Parameters to pass to the DB query (e.g., filters).

        Returns:
            Any: Data retrieved from Redis or the query result cached in Redis.

        Raises:
            RedisClientException: If the DB query or Redis operation fails.
        """
        redis_store = cls._redis_store(access_pattern.redis_store_enum)
        cached_data = cls._get_cached_data(redis_store=redis_store, redis_key=access_pattern.redis_key_enum)
        if cached_data is not None:
            unpickled_data = cls._unpickle(cached_data)
            return unpickled_data

        # Cache miss, fetch from DB
        try:
            logger.debug(f"Cache miss for key: `{access_pattern.redis_key_enum}`. Fetching from DB...")
            db_data = access_pattern.query(**(query_params or {}))
            pickled_data = cls._pickle(db_data)
            redis_store.set(
                key=access_pattern.redis_key_enum.value,
                value=pickled_data,
                timeout=access_pattern.key_ttl_enum.value,
            )
            logger.debug(
                f"Key `{access_pattern.redis_key_enum}` updated in Redis with TTL=`{access_pattern.key_ttl_enum}`"
            )
            return db_data
        except Exception as e:
            logger.error(
                f"Error fetching data for key `{access_pattern.redis_key_enum}` from DB: {e}",
                exc_info=True,
            )
            raise RedisClientException("Failed to fetch and cache data.") from e

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