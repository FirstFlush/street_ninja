from sms.tests.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage
from sms.resolvers.params.param_mappings.food import FoodParamKey
from sms.resolvers.params.enums import BooleanParamValue
from sms.resolvers.params import ParamDict


FOOD_PARAMS_INQUIRIES = [
    InquirySample(
        message="905 Main St meal",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("905 Main St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.MEALS: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="free meals 123 E Hastings St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("123 E Hastings St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.MEALS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="grocery hampers 1500 Main St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1500 Main St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.HAMPERS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="wheelchair accessible food 450 Powell St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("450 Powell St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.WHEELCHAIR: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="takeout meals near 789 Broadway",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("789 Broadway", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.TAKEOUT: BooleanParamValue.TRUE,
            FoodParamKey.MEALS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="food delivery service 987 Commercial Dr",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("987 Commercial Dr", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.DELIVER: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="takeaway and meals 222 Union St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("222 Union St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.TAKEOUT: BooleanParamValue.TRUE,
            FoodParamKey.MEALS: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="groceries and delivery 305 Keefer St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("305 Keefer St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.HAMPERS: BooleanParamValue.TRUE,
            FoodParamKey.DELIVER: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="wheelchair friendly takeout food 644 Kingsway",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("644 Kingsway", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
            FoodParamKey.TAKEOUT: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="meals delivered 858 E Broadway",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("858 E Broadway", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.MEALS: BooleanParamValue.TRUE,
            FoodParamKey.DELIVER: BooleanParamValue.TRUE
        })
    ),
    InquirySample(
        message="wheelchair accessible groceries 120 Water St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.FOOD, LanguageEnum.ENGLISH),
        location=ResolvedLocation("120 Water St", LocationType.ADDRESS),
        params=ParamDict({
            FoodParamKey.WHEELCHAIR: BooleanParamValue.TRUE,
            FoodParamKey.HAMPERS: BooleanParamValue.TRUE
        })
    ),
]




