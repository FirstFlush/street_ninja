from sms.tests.resolvers.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage


SHELTER_INQUIRIES = [
    InquirySample(
        message="620 Clark Dr bed",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("620 Clark Dr", LocationType.ADDRESS),
    ),
    InquirySample(
        message="101 E 7th Ave shelter",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("101 E 7th Ave", LocationType.ADDRESS),
    ),
    InquirySample(
        message="4125 Main St sleep",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("4125 Main St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="SHELTER 188 Alexander St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("188 Alexander St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="#5-99 Commercial Dr homeless",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("#5-99 Commercial Dr", LocationType.ADDRESS),
    ),
    InquirySample(
        message="need shelter by victory square",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("victory square", LocationType.LANDMARK),
    ),
    InquirySample(
        message="homeless. anything around 34th ave?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("34th ave", LocationType.ADDRESS),
    ),
    InquirySample(
        message="sleep needed. close to 620 clark dr",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("620 clark dr", LocationType.ADDRESS),
    ),
    InquirySample(
        message="bed near pender and carrall",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("pender and carrall", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="what's around main & 49th? i need a bed",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("main & 49th", LocationType.INTERSECTION),
    ),
]
