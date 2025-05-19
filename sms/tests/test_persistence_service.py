from faker import Faker
import pytest
from django.contrib.gis.geos import Point
from geo.models import Location
from sms.resolvers.dataclasses import ResolvedSMS
from sms.resolvers.sms_resolver import ResolvedSMSInquiry, ResolvedSMSFollowUp, UnresolvedSMS
from sms.enums import ResolvedSMSType
from sms.models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry, Conversation, PhoneNumber
from sms.persistence_service import PersistenceService
from .test_schemas import InquirySample, FollowUpSample, UnresolvedSample
from .testdata.inquiries import ALL_INQUIRIES
from .testdata.follow_up import FOLLOWUP_INQUIRIES
from .testdata.unresolved import UNRESOLVED_INQUIRIES


fake = Faker()


@pytest.mark.parametrize("sample", ALL_INQUIRIES)
@pytest.mark.django_db
def test_save_inquiry(sample: InquirySample):
    test_point = Point(-123.0990097, 49.2826649)    # 222 Main St
    test_phone_number = fake.msisdn()

    location = Location.objects.create(
        location_text=sample.location.location,
        location_type=sample.location.location_type.value,
        location=test_point,
    )
    resolved_sms_inquiry = ResolvedSMSInquiry(
        msg=sample.message,
        keyword_language_data=sample.keyword_and_language,
        location_data=sample.location,
        params=sample.params
    )
    resolved_sms = ResolvedSMS(
        resolved_sms_type=ResolvedSMSType.INQUIRY,
        phone_number=test_phone_number,
        data=resolved_sms_inquiry,
    )

    persistence_service = PersistenceService(
        sms_data=resolved_sms,
        inquiry_location=location,
    )

    persistence_service.save_sms()
    assert isinstance(persistence_service.instance, SMSInquiry)
    assert isinstance(persistence_service.conversation, Conversation)
    assert isinstance(persistence_service.phone_number, PhoneNumber)



@pytest.mark.parametrize("sample", FOLLOWUP_INQUIRIES)
@pytest.mark.django_db
def test_save_followup(sample: FollowUpSample):

    test_phone_number = fake.msisdn()
    resolved_sms_followup = ResolvedSMSFollowUp(
        msg=sample.message,
        follow_up_keyword_enum=sample.follow_up_enum,
        follow_up_params=sample.params,
    )    
    resolved_sms = ResolvedSMS(
        resolved_sms_type=ResolvedSMSType.FOLLOW_UP,
        phone_number=test_phone_number,
        data=resolved_sms_followup,
    )
    persistence_service = PersistenceService(sms_data=resolved_sms)
    persistence_service.save_sms()

    assert isinstance(persistence_service.instance, SMSFollowUpInquiry)
    assert isinstance(persistence_service.conversation, Conversation)
    assert isinstance(persistence_service.phone_number, PhoneNumber)


@pytest.mark.parametrize("sample", UNRESOLVED_INQUIRIES)
@pytest.mark.django_db
def test_save_unresolved(sample: UnresolvedSample):

    test_phone_number = fake.msisdn()
    resolved_sms_unresolved = UnresolvedSMS(msg=sample.message)
    resolved_sms = ResolvedSMS(
        resolved_sms_type=ResolvedSMSType.UNRESOLVED,
        phone_number=test_phone_number,
        data=resolved_sms_unresolved,
    )
    persistence_service = PersistenceService(sms_data=resolved_sms)

    if "\x00" in sample.message:
        with pytest.raises(ValueError):
            persistence_service.save_sms()
    else:
        persistence_service.save_sms()
        assert isinstance(persistence_service.instance, UnresolvedSMSInquiry)
        assert isinstance(persistence_service.conversation, Conversation)
        assert isinstance(persistence_service.phone_number, PhoneNumber)

