import logging
import pickle
from typing import Type, TYPE_CHECKING
from resources.abstract_models import ResourceQuerySet
from .base_redis_client import BaseRedisClient
from ..enums import RedisStoreEnum

from ..exc import RedisClientException

if TYPE_CHECKING:
    from ..access_patterns.base_access_patterns import AccessPatternDB


logger = logging.getLogger(__name__)


class ResourceCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.RESOURCES

    def __init__(self, access_pattern: Type["AccessPatternDB"]):
        super().__init__(access_pattern=access_pattern)
        self.access_pattern: "AccessPatternDB"
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



    def get_or_set_db(self, query_params: dict = None) -> ResourceQuerySet:
        """
        Fetch data from Redis if available; otherwise, query the database and cache the result.

        Raises:
            RedisClientException: If the DB query or Redis operation fails.
        """
        cached_data = self._get_cached_data(redis_key=self.access_pattern.redis_key_enum)
        if cached_data is not None:
            unpickled_data = self._unpickle(cached_data)
            if isinstance(unpickled_data, ResourceQuerySet) and len(unpickled_data) > 0:
                logger.info(f"Unpickled `{len(unpickled_data)}` resuts.")
            else:
                logger.warning(f"Problem unpickling! unpickled_data type: `{type(unpickled_data)}`, length: `{len(unpickled_data)}`")
            return unpickled_data

        # Cache miss, fetch from DB
        try:
            logger.info(f"Cache miss for key: `{self.access_pattern.redis_key_enum}`. Fetching from DB...")
            db_data = self.access_pattern.query(**(query_params or {}))
            pickled_data = self._pickle(db_data)
            self.redis_store.set(
                key=self.access_pattern.redis_key_enum.value,
                value=pickled_data,
                timeout=self.access_pattern.key_ttl_enum.value,
            )
            logger.info(
                f"Key `{self.access_pattern.redis_key_enum}` updated in Redis with TTL=`{self.access_pattern.key_ttl_enum}`"
            )
            return db_data
        except Exception as e:
            logger.error(
                f"Error fetching data for key `{self.access_pattern.redis_key_enum}` from DB: {e}",
                exc_info=True,
            )
            raise RedisClientException("Failed to fetch and cache data.") from e

