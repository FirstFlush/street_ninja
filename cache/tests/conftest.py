import pytest
from django.core.cache import caches
from cache.redis.enums import RedisStoreEnum
from cache.redis.clients import PhoneSessionCacheClient
from street_ninja_server.tests.access_patterns import PhoneSessionAccessPatternTest
from cache.inquiry_caching_service import InquiryCachingService


@pytest.fixture
def flush_redis():
    redis_cache = caches[RedisStoreEnum.TESTS.value]
    redis_cache.clear()
    yield
    redis_cache.clear()

@pytest.fixture
def phone_session_cache_client(flush_redis):
    # Redis is flushed automatically before each test using dependency injection
    return PhoneSessionCacheClient(
        redis_key=PhoneSessionAccessPatternTest.key_ttl_enum.value,
        access_pattern=PhoneSessionAccessPatternTest
    )


# @pytest.fixture
# def inquiry_cacing_service(flush_redis):
#     return InquiryCachingService(
        
        
#         phone_session_cache_client
#     )