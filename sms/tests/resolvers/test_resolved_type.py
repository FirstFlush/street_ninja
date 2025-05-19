import pytest
from sms.enums import ResolvedSMSType
from sms.resolvers.sms_resolver import SMSResolver
from ..testdata.inquiries.testdata_all_inquiries import ALL_INQUIRIES
from ..testdata.follow_up import FOLLOWUP_INQUIRIES
from ..testdata.unresolved import UNRESOLVED_INQUIRIES


def create_registry() -> list[tuple[str, ResolvedSMSType]]:
    registry = []
    registry.extend([(inquiry.message, ResolvedSMSType.INQUIRY) for inquiry in ALL_INQUIRIES])
    registry.extend([(inquiry.message, ResolvedSMSType.FOLLOW_UP) for inquiry in FOLLOWUP_INQUIRIES])
    registry.extend([(inquiry.message, ResolvedSMSType.UNRESOLVED) for inquiry in UNRESOLVED_INQUIRIES])
    return registry


@pytest.mark.parametrize("sample", create_registry())
def test_resolved_sms_enum_type(sample: tuple[str, ResolvedSMSType]):
    sms_resolver = SMSResolver(msg=sample[0])
    phone_number = "604-555-1234"
    message_sid = "abcdef"
    resolved_sms = sms_resolver.resolve_sms(
        message_sid=message_sid,
        phone_number=phone_number,
    )

    assert resolved_sms.resolved_sms_type.value == sample[1].value