from sms.tests.resolvers.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage


WIFI_INQUIRIES = [
    InquirySample(
        message="wifi 200 W Hastings St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("200 W Hastings St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="INTERNET 330 E Broadway",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("330 E Broadway", LocationType.ADDRESS),
    ),
    InquirySample(
        message="1455 Quebec St WIFI",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1455 Quebec St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="#4-827 Seymour St ONLINE",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("#4-827 Seymour St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="567 Hornby St wireless",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("567 Hornby St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="wifi access near 100 terminal ave",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("100 terminal ave", LocationType.ADDRESS),
    ),
    InquirySample(
        message="internet spot at joyce & kingsway?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("joyce & kingsway", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="need to get online at hastings & princess",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("hastings & princess", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="wireless signal around city hall?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("city hall", LocationType.LANDMARK),
    ),
    InquirySample(
        message="any public wifi by broadway skytrain",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WIFI, LanguageEnum.ENGLISH),
        location=ResolvedLocation("broadway skytrain", LocationType.LANDMARK),
    ),
]
