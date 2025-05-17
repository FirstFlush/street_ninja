# tests/conftest.py

import pytest
from django.core.management import call_command
from django.conf import settings
from django.core.cache import caches
from cache.redis.enums import RedisStoreEnum



@pytest.fixture
def flush_redis():
    redis_cache = caches[RedisStoreEnum.TESTS.value]
    redis_cache.clear()
    yield
    redis_cache.clear()


@pytest.fixture(scope="session")
def preload_all_resources(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_shelters.json")
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_food.json")
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_water.json")
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_toilet.json")
