import pytest
from sms.resolvers.location import LocationResolver, ResolvedLocation
from ..testdata.inquiries import ALL_INQUIRIES
from sms.tests.test_schemas import InquirySample


@pytest.mark.django_db()
@pytest.mark.parametrize("sample", ALL_INQUIRIES)
def test_location_resolver(sample: InquirySample, preload_all_resources):
    resolved = LocationResolver.resolve_location(msg=sample.message)
    assert isinstance(resolved, ResolvedLocation)
    assert resolved.location.lower() == sample.location.location.lower()
    assert resolved.location_type == sample.location.location_type

