from sms.tests.test_schemas import InquirySample, ResolvedKeywordAndLanguage, ResolvedLocation
from common.enums import LanguageEnum, LocationType
from sms.enums import SMSKeywordEnum


NEIGHBORHOOD_INQUIRIES_SIMPLE = [
    InquirySample(
        message="shaughnessy food",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Shaughnessy", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="kitsilano water",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Kitsilano", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="mount pleasant shelter",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Mount Pleasant", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="downtown food",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Downtown", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="grandview-woodland toilet",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Grandview-Woodland", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="west end shelter",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("West End", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="sunset food",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Sunset", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="marpole water",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Marpole", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="riley park shelter",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Riley Park", LocationType.NEIGHBORHOOD),
    ),
    InquirySample(
        message="victoria-fraserview water",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("Victoria-Fraserview", LocationType.NEIGHBORHOOD),
    ),
]
