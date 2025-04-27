from .base_access_patterns import BaseRedisAccessPattern
from ..enums import RedisStoreEnum, RedisKeyTTL, LocationKeyEnum


class LocationMapAccessPattern(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.LOCATION
    redis_key_enum = LocationKeyEnum.MAPPING
    key_ttl_enum = RedisKeyTTL.DAY