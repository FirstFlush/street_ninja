import pytest
from sms.resolvers import SMSResolver
from ..testdata.unresolved import UNRESOLVED_INQUIRIES
from sms.tests.test_schemas import UnresolvedSample


@pytest.mark.parametrize("sample", UNRESOLVED_INQUIRIES)
def test_unresolved_inquiries(sample: UnresolvedSample):
    sms_resolver = SMSResolver(msg=sample.message)
    phone_number = "604-555-1234"
    message_sid = "abcdef"
    resolved_sms = sms_resolver.resolve_sms(
        message_sid=message_sid,
        phone_number=phone_number,
    )

    assert resolved_sms.resolved_sms_type == sample.sms_type
