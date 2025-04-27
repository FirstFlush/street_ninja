import pytest
from .testdata_locations import test_location_data
from django.contrib.gis.geos import Point
from sms.resolvers.location import ResolvedLocation
from common.enums import LocationType
from geo.location_service import LocationService




# @pytest.mark.django_db
# @pytest.mark.parametrize("location_text, point", test_location_data)
# def test_get_and_update_location(
#     location_service: LocationService,
#     location_text: str,
#     point: Point,
# ):



@pytest.mark.django_db
@pytest.mark.parametrize("location_text, point", test_location_data)
def test_create_new_location_adds_to_cache_and_creates_inquiry(
    location_service: LocationService,
    location_text: str,
    point: Point,
):
    # Arrange
    resolved_location = ResolvedLocation(
        location=location_text,
        location_type=LocationType.ADDRESS,
    )

    # Act
    location = location_service.new_location(resolved_location, point)

    # Assert
    assert location is not None
    assert location.count_hits() == 1
    normalized = location_service._normalize_text(resolved_location.location)
    mapping = location_service._get_mapping()
    assert normalized in mapping
    assert mapping[normalized] == location.id
