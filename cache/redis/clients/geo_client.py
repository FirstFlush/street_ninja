import logging
from geo.neighborhoods.dataclasses import NeighborhoodCacheData
from geo.models import Neighborhood
from .base_redis_client import BaseRedisClient
from .base_model_client import BaseModelCacheClient
from ..access_patterns.geo import LocationMapAccessPattern, NeighborhoodAccessPattern

logger = logging.getLogger(__name__)


class LocationCacheClient(BaseRedisClient):

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


class NeighborhoodCacheClient(BaseModelCacheClient):

    def __init__(self):
        super().__init__(access_pattern=NeighborhoodAccessPattern)

    def get_neighborhoods(self) -> list[NeighborhoodCacheData]:
        neighborhoods = self.get_or_set_db()
        if not neighborhoods:
            neighborhoods = self.set_cache_from_db()
        return neighborhoods

    def set_neighborhoods(self) -> list[NeighborhoodCacheData]:
        return self.set_cache_from_db()
