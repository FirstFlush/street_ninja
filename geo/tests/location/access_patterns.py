from cache.redis.access_patterns.base_access_patterns import BaseRedisAccessPattern
from cache.redis.enums import RedisStoreEnum, RedisKeyTTL, TestKeyEnum


class LocationMapAccessPatternTest(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.TESTS
    redis_key_enum = TestKeyEnum.MAPPING
    key_ttl_enum = RedisKeyTTL.DAY

