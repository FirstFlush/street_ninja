import pytest
from rest_framework.test import APIClient
from django.core.management import call_command
from django.conf import settings


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def preload_all_resources(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_shelters.json")
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_food.json")
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_water.json")
        call_command("loaddata", f"{settings.BASE_DIR}/street_ninja_server/tests/testdata/model_dumps/testdata_toilet.json")