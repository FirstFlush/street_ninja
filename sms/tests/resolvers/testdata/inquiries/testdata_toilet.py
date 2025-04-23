from sms.tests.resolvers.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage



TOILET_INQUIRIES = [
    InquirySample(
        message="3580 W 41st Ave TOILET",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("3580 W 41st Ave", LocationType.ADDRESS),
    ),
    InquirySample(
        message="150 Robson St gotta pee",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("150 Robson St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="700 Granville St gotta shit",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("700 Granville St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="washroom #201-2211 Alberta St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("2211 Alberta St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="bathroom 1985 Commercial Dr",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1985 Commercial Dr", LocationType.ADDRESS),
    ),
    InquirySample(
        message="where's the nearest bathroom to 500 granville",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("500 granville", LocationType.ADDRESS),
    ),
    InquirySample(
        message="need toilet - i'm near broadway station",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("broadway station", LocationType.LANDMARK),
    ),
    InquirySample(
        message="washroom around 6th and cambie?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("6th and cambie", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="any public restroom by science world",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("science world", LocationType.LANDMARK),
    ),
    InquirySample(
        message="gotta pee. close to 33rd & main",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("33rd & main", LocationType.INTERSECTION),
    ),
]
