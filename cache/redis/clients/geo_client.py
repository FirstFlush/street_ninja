import logging
from .base_redis_client import BaseRedisClient
from ..enums import RedisStoreEnum
from ..access_patterns.geo import LocationMapAccessPattern, NeighborhoodAccessPattern

logger = logging.getLogger(__name__)


class LocationCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.GEO
    access_pattern: LocationMapAccessPattern
    
    def __init__(self, access_pattern: LocationMapAccessPattern):
        super().__init__(access_pattern=access_pattern)

    def get_mapping(self) -> dict[str, int] | None:
        return self._get_cached_data(redis_key=self.access_pattern.redis_key_enum)

    def set_mapping(self, mapping: dict[str, int]):
        self.redis_store.set(
            key=self.access_pattern.redis_key_enum.value, 
            value=mapping, 
            timeout=self.access_pattern.key_ttl_enum.value
        )

class NeighborhoodCacheClient(BaseRedisClient):

    redis_store_enum = RedisStoreEnum.GEO
    access_pattern: NeighborhoodAccessPattern

    def __init__(self, access_pattern: NeighborhoodAccessPattern):
        super().__init__(access_pattern=access_pattern)

    def get_neighborhoods(self):
        self._get_cached_data(redis_key=self.access_pattern.redis_key_enum)
        #TODO

    def set_neighborhoods(self):
        #TODO
        ...