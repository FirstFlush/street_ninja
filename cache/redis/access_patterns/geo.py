from .base_access_patterns import BaseRedisAccessPattern, AccessPatternDB
from ..enums import RedisStoreEnum, RedisKeyTTL, GeoKeyEnum
from geo.models import Neighborhood
from geo.neighborhoods.dataclasses import NeighborhoodCacheData

class LocationMapAccessPattern(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.GEO
    redis_key_enum = GeoKeyEnum.LOCATION_MAPPING
    key_ttl_enum = RedisKeyTTL.DAY


class NeighborhoodAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.GEO
    redis_key_enum = GeoKeyEnum.NEIGHBORHOODS
    key_ttl_enum = RedisKeyTTL.DAY
    expected_type = NeighborhoodCacheData
    query = Neighborhood.objects.cache_data