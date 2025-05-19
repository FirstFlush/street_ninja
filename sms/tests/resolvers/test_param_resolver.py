import pytest
from sms.resolvers.dataclasses import ParamDict
from sms.resolvers.params.param_resolver import ParamResolver
from sms.tests.test_schemas import InquirySample
from ..testdata.inquiries import ALL_INQUIRIES


@pytest.mark.parametrize("sample", ALL_INQUIRIES)
def test_param_resolver(sample: InquirySample):
    resolved = ParamResolver.resolve_params(
        msg=sample.message, 
        sms_keyword_enum=sample.keyword_and_language.sms_keyword_enum
    )

    assert isinstance(resolved, ParamDict)
    if resolved.params:
        assert resolved.params == sample.params.params if resolved.params else None
