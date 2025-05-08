import pytest
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage, KeywordLanguageResolver
from sms.tests.test_schemas import InquirySample
from ..testdata.inquiries import ALL_INQUIRIES


@pytest.mark.parametrize("sample", ALL_INQUIRIES)
def test_keyword_and_language_resolver(sample: InquirySample):
    resolved = KeywordLanguageResolver.get_keyword_and_language(msg=sample.message)
    
    assert isinstance(resolved, ResolvedKeywordAndLanguage)
    assert resolved.sms_keyword_enum == sample.keyword_and_language.sms_keyword_enum
    assert resolved.language_enum == sample.keyword_and_language.language_enum