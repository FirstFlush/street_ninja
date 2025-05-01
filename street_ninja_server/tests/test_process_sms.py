import pytest
from _pytest.monkeypatch import MonkeyPatch
from typing import Type
from resources.models import Shelter, FoodProgram, Toilet, DrinkingFountain, PublicWifi
from sms.sms_service import SMSService
from django.contrib.gis.geos import Point
from geo.models import Location
from common.enums import LocationType
from street_ninja_server.global_mappings import ACCESS_PATTERN_TO_MODEL
from cache.redis.clients.resource_client import ResourceCacheClient
from cache.redis.access_patterns import (
    FoodProgramAccessPattern,
    ShelterAccessPattern,
    DrinkingFountainAccessPattern,
    ToiletAccessPattern,
    PublicWifiAccessPattern,
)


def get_location_monkeypatch(self) -> Location:
    return Location.objects.create(
        location=Point(-123.1, 49.28),
        location_text="222 main st",
        location_type=LocationType.ADDRESS.value,
    )

def geocode_monkeypatch(self) -> Point:
    return Point(-123.1, 49.28)

def get_or_set_db_monkeypatch(self: ResourceCacheClient) -> list[FoodProgram]:
    try:
        model = ACCESS_PATTERN_TO_MODEL[self.access_pattern]
    except Exception as e:
        pytest.fail(f"Invalid access pattern, can not monkeypatch: `{self.access_pattern}`")
    else:
        return list(model.objects.filter(is_active=True))


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
    
    assert len(response) < 459  # 153 chars x 3 = 459. SMS limits to 160/msg. When multiple sms msgs are strung together, its 153/msg with 7 chars reserved for metadata.