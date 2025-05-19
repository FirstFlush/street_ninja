from cache.redis.access_patterns.base_access_patterns import BaseRedisAccessPattern, AccessPatternDB
from cache.redis.enums import RedisStoreEnum, RedisKeyTTL, TestKeyEnum
from geo.models import Neighborhood


class LocationMapAccessPatternTest(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.TESTS
    redis_key_enum = TestKeyEnum.LOCATION_MAPPING
    key_ttl_enum = RedisKeyTTL.DAY
    

class NeighborhoodAccessPatternTest(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.TESTS
    redis_key_enum = TestKeyEnum.NEIGHBORHOODS
    key_ttl_enum = RedisKeyTTL.DAY
    model_cls = Neighborhood
    query = Neighborhood.objects.cache_data