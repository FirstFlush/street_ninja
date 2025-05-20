import pytest
from django.core.management import call_command
from django.conf import settings


@pytest.fixture(scope="session")
def preload_all_resources(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", f"{settings.BASE_DIR}/sms/tests/testdata/testdata_neighborhoods_from_db.json")
