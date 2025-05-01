import pytest
from _pytest.monkeypatch import MonkeyPatch
from resources.models import Shelter, FoodProgram, Toilet, DrinkingFountain
from sms.sms_service import SMSService
from django.contrib.gis.geos import Point
from geo.models import Location
from common.enums import LocationType
from cache.redis.clients.resource_client import ResourceCacheClient


def get_location_monkeypatch(self) -> Location:
    return Location.objects.create(
        location=Point(-123.1, 49.28),
        location_text="222 main st",
        location_type=LocationType.ADDRESS.value,
    )

def geocode_monkeypatch(self) -> Point:
    return Point(-123.1, 49.28)

def get_or_set_db_monkeypatch(self) -> list[FoodProgram]:
    return list(FoodProgram.objects.filter(is_active=True))


@pytest.mark.django_db
def test_process_sms(client, preload_all_resources, monkeypatch: MonkeyPatch):

    monkeypatch.setattr(SMSService, "get_location", get_location_monkeypatch)
    monkeypatch.setattr(SMSService, "geocode", geocode_monkeypatch)
    monkeypatch.setattr(ResourceCacheClient, "get_or_set_db", get_or_set_db_monkeypatch)

    response = SMSService.process_sms(
        msg="food 222 main st",
        phone_number="6045551234",
        message_sid="0123456789abcdef"
    )


    print(response)
