import pytest
from _pytest.monkeypatch import MonkeyPatch
from resources.abstract_models import ResourceModel
from sms.sms_service import SMSService
from django.contrib.gis.geos import Point
from geo.models import Location
from common.enums import LocationType
from street_ninja_server.global_mappings import ACCESS_PATTERN_TO_MODEL
from cache.redis.clients.resource_client import ResourceCacheClient


inquiry_location = Point(-123.0990097, 49.2826649)  # 222 main st
sms_test_cases = (
    ("222 main st food", "Food on the Corner"),
    ("222 main st shelter", "The Haven"),
    ("222 main st toilet", "Powell at Main"),
    ("222 main st water", "Powell & Gore"),
)

def get_location_monkeypatch(self) -> Location:
    return Location.objects.get_or_create(
        location=inquiry_location,
        location_text="222 main st",
        location_type=LocationType.ADDRESS.value,
    )[0]

def geocode_monkeypatch(self) -> Point:
    return inquiry_location

def get_or_set_db_monkeypatch(self: ResourceCacheClient) -> list[ResourceModel]:
    try:
        model = ACCESS_PATTERN_TO_MODEL[self.access_pattern]
    except Exception as e:
        pytest.fail(f"Invalid access pattern, can not monkeypatch: `{self.access_pattern}`")
    else:
        return list(model.objects.filter(is_active=True))


@pytest.mark.parametrize("sample", sms_test_cases)
@pytest.mark.django_db
def test_process_sms(client, preload_all_resources, monkeypatch: MonkeyPatch, sample: tuple[str, str]):

    monkeypatch.setattr(SMSService, "_get_location", get_location_monkeypatch)
    monkeypatch.setattr(SMSService, "_geocode", geocode_monkeypatch)
    monkeypatch.setattr(ResourceCacheClient, "get_or_set_db", get_or_set_db_monkeypatch)

    response = SMSService.process_sms(
        msg=sample[0],
        phone_number="6045551234",
        message_sid="0123456789abcdef"
    )

    assert len(response) < 459  # 153 chars x 3 = 459. Under 459 means we are under 3 segments
    assert sample[1] in response