from sms.tests.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage


WATER_INQUIRIES = [
    InquirySample(
        message="201 Burrard St water",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("201 Burrard St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="#102-1333 W Broadway hydrate",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1333 W Broadway", LocationType.ADDRESS),
    ),
    InquirySample(
        message="drink 1200 W Georgia St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1200 W Georgia St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="250 E Pender St drinking fountain",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("250 E Pender St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="FOUNTAIN 4438 Fraser St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("4438 Fraser St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="fountains on robson near bute & davie?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("bute & davie", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="thirsty by main and terminal",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("main and terminal", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="hydration spot close to 2201 kingsway",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("2201 kingsway", LocationType.ADDRESS),
    ),
    InquirySample(
        message="where to drink near 950 e hastings?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("950 e hastings", LocationType.ADDRESS),
    ),
    InquirySample(
        message="need clean water near joyce stn",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("joyce stn", LocationType.LANDMARK),
    ),
]
