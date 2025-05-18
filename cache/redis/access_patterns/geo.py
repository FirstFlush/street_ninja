from .base_access_patterns import BaseRedisAccessPattern
from ..enums import RedisStoreEnum, RedisKeyTTL, GeoKeyEnum


class LocationMapAccessPattern(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.GEO
    redis_key_enum = GeoKeyEnum.LOCATION_MAPPING
    key_ttl_enum = RedisKeyTTL.DAY


class NeighborhoodAccessPattern(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.GEO
    redis_key_enum = GeoKeyEnum.NEIGHBORHOODS
    key_ttl_enum = RedisKeyTTL.DAY