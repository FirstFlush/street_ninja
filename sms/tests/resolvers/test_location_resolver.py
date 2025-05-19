import pytest
from sms.resolvers.location import LocationResolver, ResolvedLocation
from ..testdata.inquiries import ALL_INQUIRIES
from sms.tests.test_schemas import InquirySample


@pytest.mark.django_db
# @pytest.mark.parametrize("sample", ALL_INQUIRIES)
def test_location_resolver():
    
    from sms.tests.test_schemas import InquirySample, ResolvedKeywordAndLanguage, ResolvedLocation
    from common.enums import LanguageEnum, LocationType
    from sms.enums import SMSKeywordEnum

    from geo.models import Neighborhood
    print("DB has:", Neighborhood.objects.all().values_list('name', flat=True))
    exit(0)
    sample = InquirySample(
        message="shaughnessy food",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Shaughnessy", LocationType.NEIGHBORHOOD),
    )
    
    
    resolved = LocationResolver.resolve_location(msg=sample.message)
    assert isinstance(resolved, ResolvedLocation)
    assert resolved.location.lower() == sample.location.location.lower()
    assert resolved.location_type == sample.location.location_type


# @pytest.mark.django_db
# @pytest.mark.parametrize("sample", ALL_INQUIRIES)
# def test_location_resolver(sample: InquirySample):
#     resolved = LocationResolver.resolve_location(msg=sample.message)
#     assert isinstance(resolved, ResolvedLocation)
#     assert resolved.location.lower() == sample.location.location.lower()
#     assert resolved.location_type == sample.location.location_type

