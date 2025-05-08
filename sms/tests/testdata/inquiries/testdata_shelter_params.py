from sms.tests.test_schemas import InquirySample
from sms.enums import SMSKeywordEnum
from common.enums import LanguageEnum, LocationType
from sms.resolvers.location import ResolvedLocation
from sms.resolvers.keyword_and_language_resolver import ResolvedKeywordAndLanguage
from sms.resolvers.params.param_mappings.shelter import ShelterParamKey, ShelterCategoryParamValue
from sms.resolvers.params.enums import BooleanParamValue
from sms.resolvers.params import ParamDict


SHELTER_PARAMS_INQUIRIES = [
    InquirySample(
        message="bed for women granville and pender",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("granville and pender", LocationType.INTERSECTION),
        params=ParamDict({
            ShelterParamKey.CATEGORY: ShelterCategoryParamValue.WOMEN
        })
    ),
    InquirySample(
        message="pet friendly shelter 566 Powell St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("566 Powell St", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.PETS: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="beds 875 Terminal Ave teen",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("875 Terminal Ave", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.CATEGORY: ShelterCategoryParamValue.YOUTH,
        })
    ),
    InquirySample(
        message="womens shelter 835 E Hastings St shopping carts allowed",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("835 E Hastings St", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.CATEGORY: ShelterCategoryParamValue.WOMEN,
            ShelterParamKey.CARTS: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="pet shelter needed 3475 Cambie St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("3475 Cambie St", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.PETS: BooleanParamValue.TRUE,
        })
    ),
    InquirySample(
        message="shelter for men 1135 Granville St allows dogs",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1135 Granville St", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.PETS: BooleanParamValue.TRUE,
            ShelterParamKey.CATEGORY: ShelterCategoryParamValue.MEN
        })
    ),
    InquirySample(
        message="emergency shelter for women 1430 Burrard St",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("1430 Burrard St", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.CATEGORY: ShelterCategoryParamValue.WOMEN
        })
    ),
    InquirySample(
        message="adult shelter near 63 keefer pl",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("63 keefer pl", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.CATEGORY: ShelterCategoryParamValue.ADULTS,
        })
    ),
    InquirySample(
        message="620 Clark Dr bed pets and shopping-carts allowed",
        keyword_and_language=ResolvedKeywordAndLanguage(SMSKeywordEnum.SHELTER, LanguageEnum.ENGLISH),
        location=ResolvedLocation("620 Clark Dr", LocationType.ADDRESS),
        params=ParamDict({
            ShelterParamKey.PETS: BooleanParamValue.TRUE,
            ShelterParamKey.CARTS: BooleanParamValue.TRUE,
        })

    ),

]