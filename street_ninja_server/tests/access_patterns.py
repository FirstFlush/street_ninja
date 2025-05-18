from cache.redis.access_patterns.base_access_patterns import BaseRedisAccessPattern
from cache.redis.enums import RedisStoreEnum, RedisKeyTTL, TestKeyEnum


class LocationMapAccessPatternTest(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.TESTS
    redis_key_enum = TestKeyEnum.LOCATION_MAPPING
    key_ttl_enum = RedisKeyTTL.DAY


class PhoneSessionAccessPatternTest(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.TESTS
    redis_key_enum = TestKeyEnum.PHONE_SESSION
    key_ttl_enum = RedisKeyTTL.HOUR