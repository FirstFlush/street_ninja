from sms.tests.resolvers.test_schemas import InquirySample
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
]