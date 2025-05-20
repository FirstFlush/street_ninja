import pytest
from geo.location_service import LocationService
from geo.neighborhoods.neighborhood_service import NeighborhoodService
from django.core.cache import caches
from cache.redis.enums import RedisStoreEnum
from .location.access_patterns import LocationMapAccessPatternTest

@pytest.fixture
def flush_redis():
    redis_cache = caches[RedisStoreEnum.TESTS.value]
    redis_cache.clear()
    yield
    redis_cache.clear()


@pytest.fixture
def neighborhood_service(flush_redis):
    return NeighborhoodService()


@pytest.fixture
def location_service(flush_redis):
    # Redis is flushed automatically before each test using dependency injection
    return LocationService(access_pattern=LocationMapAccessPatternTest)
