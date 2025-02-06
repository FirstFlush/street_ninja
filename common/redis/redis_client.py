from abc import ABC
import json
import logging
from django.core.cache import cache, caches
from django.core.cache.backends.base import BaseCache
import pickle
from typing import Any, Type
from .enums import RedisStoreEnum, RedisKeyEnum
from .exc import RedisClientException, InvalidAccessPattern
from .access_patterns import *
from .access_patterns.base_access_patterns import BaseRedisAccessPattern

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
            logger.error(f"Error fetching key `{redis_key}` from Redis: {e}", exc_info=True)
            if raise_error:
                raise
        return None


    def _validate_access_pattern_type(self, expected_type:Type["BaseRedisAccessPattern"]):

        print()
        print()
        print(self.access_pattern)
        print(expected_type)
        print()
        print()

        if not isinstance(self.access_pattern, expected_type):
            error_msg = f"Access pattern must be of type AccessPatternDB, not `{type(self.access_pattern).__name__}`"
            logger.error(error_msg)
            raise RedisClientException("RedisClient failed due to an invalid access pattern.") from InvalidAccessPattern(error_msg)





    # @staticmethod
    # def _redis_store(redis_store_enum: RedisStoreEnum) -> BaseCache:
    #     """
    #     Retrieve the appropriate Redis store for the given Redis store enum.

    #     Args:
    #         redis_store_enum (RedisStoreEnum): The Redis store to access.

    #     Returns:
    #         BaseCache: The Redis store backend associated with the store enum.

    #     Raises:
    #         RedisClientException: If the Redis store cannot be found.
    #     """
    #     try:
    #         return caches[redis_store_enum.value]
    #     except KeyError as e:
    #         logger.error(
    #             f"Invalid Redis store: `{redis_store_enum}`. Available stores: {list(caches)}",
    #             exc_info=True
    #         )
    #         raise RedisClientException(f"Invalid Redis store: `{redis_store_enum}`") from e

    # @staticmethod
    # def _get_cached_data(redis_store: BaseCache, redis_key: RedisKeyEnum, raise_error: bool= False) -> Any | None:
    #     """
    #     Retrieve cached data from Redis.

    #     Args:
    #         redis_store (BaseCache): The Redis store to query.
    #         redis_key (RedisKeyEnum): The Redis key to fetch.

    #     Returns:
    #         Any | None: Cached data if available, otherwise None.

    #     Logs:
    #         - Cache hit or miss.
    #         - Errors when fetching data from Redis.
    #     """
    #     try:
    #         cached_data = redis_store.get(redis_key.value)
    #         if cached_data:
    #             logger.debug(f"Cache hit for key: {redis_key}")
    #             return json.loads(cached_data) if isinstance(cached_data, str) else cached_data
    #     except Exception as e:
    #         logger.error(f"Error fetching key `{redis_key}` from Redis: {e}", exc_info=True)
    #         if raise_error:
    #             raise
    #     return None

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




class ResourceCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.RESOURCES

    def __init__(self, access_pattern: Type[AccessPatternDB]):
        super().__init__(access_pattern=access_pattern)
        # self._validate_access_pattern_type(expected_type=AccessPatternDB)
        self.access_pattern: AccessPatternDB
        self.redis_store = self._redis_store()


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



    def get_or_set_db(self, query_params: dict = None) -> Any:
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
        # redis_store = self._redis_store(self.access_pattern.redis_store_enum)
        cached_data = self._get_cached_data(redis_key=self.access_pattern.redis_key_enum)
        if cached_data is not None:
            unpickled_data = self._unpickle(cached_data)
            return unpickled_data

        # Cache miss, fetch from DB
        try:
            logger.debug(f"Cache miss for key: `{self.access_pattern.redis_key_enum}`. Fetching from DB...")
            db_data = self.access_pattern.query(**(query_params or {}))
            pickled_data = self._pickle(db_data)
            self.redis_store.set(
                key=self.access_pattern.redis_key_enum.value,
                value=pickled_data,
                timeout=self.access_pattern.key_ttl_enum.value,
            )
            logger.debug(
                f"Key `{self.access_pattern.redis_key_enum}` updated in Redis with TTL=`{self.access_pattern.key_ttl_enum}`"
            )
            return db_data
        except Exception as e:
            logger.error(
                f"Error fetching data for key `{self.access_pattern.redis_key_enum}` from DB: {e}",
                exc_info=True,
            )
            raise RedisClientException("Failed to fetch and cache data.") from e






    # @classmethod
    # def get_or_set_db(cls, access_pattern: AccessPatternDB, query_params: dict = None) -> Any:
    #     """
    #     Fetch data from Redis if available; otherwise, query the database and cache the result.

    #     Args:
    #         access_pattern (AccessPatternDB): The access pattern defining how Redis is used for this operation.
    #         query_params (dict, optional): Parameters to pass to the DB query (e.g., filters).

    #     Returns:
    #         Any: Data retrieved from Redis or the query result cached in Redis.

    #     Raises:
    #         RedisClientException: If the DB query or Redis operation fails.
    #     """
    #     redis_store = cls._redis_store(access_pattern.redis_store_enum)
    #     cached_data = cls._get_cached_data(redis_store=redis_store, redis_key=access_pattern.redis_key_enum)
    #     if cached_data is not None:
    #         unpickled_data = cls._unpickle(cached_data)
    #         return unpickled_data

    #     # Cache miss, fetch from DB
    #     try:
    #         logger.debug(f"Cache miss for key: `{access_pattern.redis_key_enum}`. Fetching from DB...")
    #         db_data = access_pattern.query(**(query_params or {}))
    #         pickled_data = cls._pickle(db_data)
    #         redis_store.set(
    #             key=access_pattern.redis_key_enum.value,
    #             value=pickled_data,
    #             timeout=access_pattern.key_ttl_enum.value,
    #         )
    #         logger.debug(
    #             f"Key `{access_pattern.redis_key_enum}` updated in Redis with TTL=`{access_pattern.key_ttl_enum}`"
    #         )
    #         return db_data
    #     except Exception as e:
    #         logger.error(
    #             f"Error fetching data for key `{access_pattern.redis_key_enum}` from DB: {e}",
    #             exc_info=True,
    #         )
    #         raise RedisClientException("Failed to fetch and cache data.") from e



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