from sms.tests.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage
from sms.resolvers.params.param_mappings.toilet import ToiletParamKey
from sms.resolvers.params.enums import BooleanParamValue
from sms.resolvers.params import ParamDict


TOILET_PARAMS_INQUIRIES = [
    InquirySample(
        message="toilet 300 Main St disabled",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("300 Main St", LocationType.ADDRESS),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="wheelchair bathroom 888 Homer St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("888 Homer St", LocationType.ADDRESS),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="restroom near hastings and carrall handicap",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("hastings and carrall", LocationType.INTERSECTION),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="public washroom 600 Robson St disability friendly",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("600 Robson St", LocationType.ADDRESS),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="pee spot 500 Beatty St wheelchairfriendly",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("500 Beatty St", LocationType.ADDRESS),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="im disabled where can i shit near main and pender",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("main and pender", LocationType.INTERSECTION),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="piss place 901 Granville St handicapped",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("901 Granville St", LocationType.ADDRESS),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="wheelchair accessible restroom 400 Richards St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("400 Richards St", LocationType.ADDRESS),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="washroom 1234 Kingsway disability",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1234 Kingsway", LocationType.ADDRESS),
        params=ParamDict({            
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="crap spot with wheelchair ramp near boundary and hastings",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.TOILET, LanguageEnum.ENGLISH),
        location=ResolvedLocation("boundary and hastings", LocationType.INTERSECTION),
        params=ParamDict({
            ToiletParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
        })
    ),
]
