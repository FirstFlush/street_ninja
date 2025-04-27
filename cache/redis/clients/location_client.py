import logging
import random
from django.contrib.sessions.backends.base import SessionBase
from .base_redis_client import BaseRedisClient
from ..enums import RedisStoreEnum
from ..access_patterns import LocationMapAccessPattern


logger = logging.getLogger(__name__)


class LocationCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.LOCATION

    def __init__(self):
        super().__init__(access_pattern=LocationMapAccessPattern)
        self.access_pattern: LocationMapAccessPattern

    def get_mapping(self) -> dict[str, int] | None:
        return self._get_cached_data(redis_key=self.access_pattern.redis_key_enum)

    def set_mapping(self, mapping: dict[str, int]):
        self.redis_store.set(
            key=self.access_pattern.redis_key_enum.value, 
            value=mapping, 
            timeout=self.access_pattern.key_ttl_enum.value
        )