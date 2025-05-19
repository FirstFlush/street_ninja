
import pytest
from sms.enums import FollowUpParams
from sms.resolvers.sms_resolver import SMSResolver
from ..testdata.follow_up import FOLLOWUP_INQUIRIES
from sms.tests.test_schemas import FollowUpSample


@pytest.mark.parametrize("sample", FOLLOWUP_INQUIRIES)
def test_unresolved_inquiries(sample: FollowUpSample):
    sms_resolver = SMSResolver(msg=sample.message)
    phone_number = "604-555-1234"
    message_sid = "abcdef"
    resolved_sms = sms_resolver.resolve_sms(
        message_sid=message_sid,
        phone_number=phone_number,
    )

    assert resolved_sms.data.follow_up_keyword_enum.value == sample.follow_up_enum.value
    if resolved_sms.data.follow_up_params:
        assert resolved_sms.data.follow_up_params[FollowUpParams.SELECTION.value] == sample.params[FollowUpParams.SELECTION.value]