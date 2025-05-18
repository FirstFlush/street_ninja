import logging
import pickle
from typing import Any, Type
from ..exc import RedisClientException
from .base_redis_client import BaseRedisClient
from ..access_patterns.base_access_patterns import AccessPatternDB
from django.db.models import Model


logger = logging.getLogger(__name__)


class BaseModelCacheClient(BaseRedisClient):

    QUERY_PARAMS: dict[str, Any] = {}

    def __init__(self, access_pattern: Type["AccessPatternDB"]):
        super().__init__(access_pattern=access_pattern)
        self.access_pattern = access_pattern
        self.redis_store = self._redis_store()

    def _pickle(self, data: list) -> bytes:
        try:
            return pickle.dumps(data)
        except Exception as e:
            logger.error(f"Error pickling data: {e}", exc_info=True)
            raise RedisClientException(f"Error pickling `{self.access_pattern.model_cls.__name__}`") from e

    def _unpickle(self, data: bytes) -> list:
        try:
            return pickle.loads(data)
        except Exception as e:
            logger.error(f"Error unpickling data: {e}", exc_info=True)
            raise RedisClientException(f"Error unpickling binary data of size `{len(data)}` bytes.") from e

    def _to_list(self, qs) -> list:
        if isinstance(qs, list):
            return qs
        if hasattr(qs, "__iter__"):
            return list(qs)
        msg = f"{self.__class__.__name__} received invalid queryset type: {type(qs)}"
        raise RedisClientException(msg)


    def set_cache_from_db(self) -> list[Model]:
        try:
            db_data = self.access_pattern.query(**self.QUERY_PARAMS)
            list_data = self._to_list(db_data)
            pickled_data = self._pickle(list_data)
            self.redis_store.set(
                key=self.access_pattern.redis_key_enum.value,
                value=pickled_data,
                timeout=self.access_pattern.key_ttl_enum.value,
            )
            return list_data
        except Exception as e:
            logger.error(f"Failed to query/cache: {e}", exc_info=True)
            raise RedisClientException("DB fallback failed.") from e


    def get_or_set_db(self) -> list[Model]:
        cached_data = self._get_cached_data(redis_key=self.access_pattern.redis_key_enum)
        if cached_data:
            result = self._unpickle(cached_data)
            if isinstance(result, list) and all(isinstance(i, self.access_pattern.model_cls) for i in result):
                return result
            logger.warning("Unpickled data structure/type mismatch. Refetching from DB...")

        # Fallback to DB
        return self.set_cache_from_db()
