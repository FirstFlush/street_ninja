import pytest
from sms.resolvers.location import LocationResolver, ResolvedLocation
from .testdata_location_resolver import LOCATION_SAMPLES

@pytest.mark.parametrize("msg,expected_loc,expected_type", LOCATION_SAMPLES)
def test_location_resolver(msg, expected_loc, expected_type):
    resolved = LocationResolver.resolve_location(msg)
    assert isinstance(resolved, ResolvedLocation)
    assert resolved.location.lower() == expected_loc.lower()
    assert resolved.location_type == expected_type
