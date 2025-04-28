from sms.tests.resolvers.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage
from sms.resolvers.params.param_mappings.water import WaterParamKey
from sms.resolvers.params.enums import BooleanParamValue
from sms.resolvers.params import ParamDict


WATER_PARAMS_INQUIRIES = [
    InquirySample(
        message="water fountain handicap and pet friendly 800 Robson St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("800 Robson St", LocationType.ADDRESS),
        params=ParamDict({
            WaterParamKey.PETS: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="hydration station near cambie and broadway petfriendly",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("cambie and broadway", LocationType.INTERSECTION),
        params=ParamDict({
            WaterParamKey.PETS: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="thirsty need drinking fountain 333 Seymour St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("333 Seymour St", LocationType.ADDRESS),
        params=ParamDict({})
    ),
    InquirySample(
        message="dog friendly water fountain 970 Burrard St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("970 Burrard St", LocationType.ADDRESS),
        params=ParamDict({
            WaterParamKey.PETS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="hydration fountain for pets 1622 Commercial Dr",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1622 Commercial Dr", LocationType.ADDRESS),
        params=ParamDict({
            WaterParamKey.PETS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="fountain near hastings and columbia",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("hastings and columbia", LocationType.INTERSECTION),
        params=ParamDict({})
    ),
    InquirySample(
        message="dog water fountain 1180 Pacific Blvd",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1180 Pacific Blvd", LocationType.ADDRESS),
        params=ParamDict({
            WaterParamKey.PETS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="drinking water near 200 Abbott St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("200 Abbott St", LocationType.ADDRESS),
        params=ParamDict({})
    ),
    InquirySample(
        message="hydrate station 1200 W Pender St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1200 W Pender St", LocationType.ADDRESS),
        params=ParamDict({})
    ),
    InquirySample(
        message="petfriendly fountain near 400 ross",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.WATER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("400 ross", LocationType.ADDRESS),
        params=ParamDict({
            WaterParamKey.PETS: BooleanParamValue.TRUE
        })
    ),
]
