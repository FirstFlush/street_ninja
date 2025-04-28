import pytest

from django.contrib.gis.geos import Point
from sms.resolvers.location import ResolvedLocation
from common.enums import LocationType
from geo.location_service import LocationService
from .testdata_factories import generate_bulk_fake_locations


@pytest.mark.django_db
@pytest.mark.parametrize("location_text, point", generate_bulk_fake_locations(100))
def test_check_mapping_finds_existing_location(
    location_service: LocationService,
    location_text: str,
    point: Point,
):
    resolved_location = ResolvedLocation(
        location=location_text,
        location_type=LocationType.ADDRESS
    )
    location = location_service.new_location(
        resolved_location=resolved_location,
        point=point,
    )
    location_id = location_service.check_mapping(location.location_text)
    assert location_id == location.id


@pytest.mark.django_db
@pytest.mark.parametrize("location_text, point", generate_bulk_fake_locations(100))
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
    normalized = location_service._normalize_text(resolved_location.location)
    mapping = location_service._get_mapping()
    assert normalized in mapping
    assert mapping[normalized] == location.id
