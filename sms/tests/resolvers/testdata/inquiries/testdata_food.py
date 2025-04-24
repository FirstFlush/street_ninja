from sms.tests.resolvers.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage


FOOD_INQUIRIES = [
    InquirySample(
        message="food 104 W Cordova St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("104 W Cordova St", LocationType.ADDRESS),
    ),
    # InquirySample(
    #     message="fourth ave and knight st FOOD",
    #     keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
    #     location=ResolvedLocation("fourth ave and knight st", LocationType.INTERSECTION),
    # ),
    # InquirySample(
    #     message="34th Ave and Knight St FOOD",
    #     keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
    #     location=ResolvedLocation("34th Ave and Knight St", LocationType.INTERSECTION),
    # ),
    # InquirySample(
    #     message="22nd Ave & Knight St FOOD",
    #     keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
    #     location=ResolvedLocation("22nd Ave & Knight St", LocationType.INTERSECTION),
    # ),
    InquirySample(
        message="hungry 123 Powell St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("123 Powell St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="905 Main St meal",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("905 Main St", LocationType.ADDRESS),
    ),
    InquirySample(
        message="#3-224 E 10th Ave breakfast",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("224 E 10th Ave", LocationType.ADDRESS),
    ),
    InquirySample(
        message="any food near #212-104 W Cordova?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("104 W Cordova", LocationType.ADDRESS),
    ),
    InquirySample(
        message="hungry at main and hastings",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("main and hastings", LocationType.INTERSECTION),
    ),
    InquirySample(
        message="any place to eat 222 main st",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("222 main st", LocationType.ADDRESS),
    ),
    InquirySample(
        message="brunch 101 e 7th ave",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("101 e 7th ave", LocationType.ADDRESS),
    ),
    InquirySample(
        message="food plz - 300 block powell st",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("300 block powell st", LocationType.ADDRESS),
    ),
    InquirySample(
        message="dinner options close to commercial & broadway?",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("commercial & broadway", LocationType.INTERSECTION),
    ),
]

