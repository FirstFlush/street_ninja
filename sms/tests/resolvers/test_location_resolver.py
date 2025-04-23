import pytest
from sms.resolvers.location import LocationResolver, ResolvedLocation
from .testdata.inquiries import ALL_INQUIRIES
from sms.tests.resolvers.test_schemas import InquirySample



@pytest.mark.parametrize("sample", ALL_INQUIRIES)
def test_location_resolver(sample: InquirySample):
    resolved = LocationResolver.resolve_location(msg=sample.message)
    assert isinstance(resolved, ResolvedLocation)
    assert resolved.location.lower() == sample.location.location.lower()
    assert resolved.location_type == sample.location.location_type


# @pytest.mark.parametrize("msg,expected_location,expected_type", LOCATION_SAMPLES)
# def test_location_resolver(msg, expected_location, expected_type):
#     resolved = LocationResolver.resolve_location(msg)
#     assert isinstance(resolved, ResolvedLocation)
#     assert resolved.location.lower() == expected_location.lower()
#     assert resolved.location_type == expected_type
