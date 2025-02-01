from dataclasses import dataclass
import logging
from typing import Any
from common.enums import SMSKeywordEnum, LanguageEnum, StreetNinjaEnum
from resources.enums import (
    ParamKeyEnum,
    ParamValueEnum,
    ShelterCategoryParamValue, 
    ShelterParamKey,
    BooleanParamValue,
)
from .exc import ParamResolutionError
from .base_resolver import BaseKeywordResolver


logger = logging.getLogger(__name__)


@dataclass
class ParamDict:
    params: dict[ParamKeyEnum, ParamValueEnum] = None

    def to_dict(self) -> dict[str, Any]:
        return { k.value: v for k, v in self.params.items()} if self.params else {}


class KeywordParamResolver(BaseKeywordResolver):
    
    MAPPING = {
        SMSKeywordEnum.SHELTER: {
            ShelterParamKey.CATEGORY: {
                "woman": ShelterCategoryParamValue.WOMEN,
                "women": ShelterCategoryParamValue.WOMEN,
                "womens": ShelterCategoryParamValue.WOMEN,
                "ladies": ShelterCategoryParamValue.WOMEN,
                "female": ShelterCategoryParamValue.WOMEN,
                "females": ShelterCategoryParamValue.WOMEN,
                "man": ShelterCategoryParamValue.MEN,
                "men": ShelterCategoryParamValue.MEN,
                "mens": ShelterCategoryParamValue.MEN,
                "male": ShelterCategoryParamValue.MEN,
                "males": ShelterCategoryParamValue.MEN,
                "youth": ShelterCategoryParamValue.YOUTH,
                "youths": ShelterCategoryParamValue.YOUTH,
                "kid": ShelterCategoryParamValue.YOUTH,
                "kids": ShelterCategoryParamValue.YOUTH,
                "teen": ShelterCategoryParamValue.YOUTH,
                "teens": ShelterCategoryParamValue.YOUTH,
                "teenager": ShelterCategoryParamValue.YOUTH,
                "teenagers": ShelterCategoryParamValue.YOUTH,
                "adult": ShelterCategoryParamValue.ADULTS,
                "adults": ShelterCategoryParamValue.ADULTS,
            },
            ShelterParamKey.PETS: {
                # "allergy": False,
                # "allergic": False,
                # "petallergy": False,
                "pet": BooleanParamValue.TRUE,
                "pets": BooleanParamValue.TRUE,
                "dog": BooleanParamValue.TRUE,
                "dogs": BooleanParamValue.TRUE,
                "cat": BooleanParamValue.TRUE,
                "cats": BooleanParamValue.TRUE,
                "animal": BooleanParamValue.TRUE,
                "animals": BooleanParamValue.TRUE,
                "petfriendly": BooleanParamValue.TRUE,
            },
            ShelterParamKey.CARTS: {
                "cart": BooleanParamValue.TRUE,
                "carts": BooleanParamValue.TRUE,
                "shoppingcart": BooleanParamValue.TRUE,
                "shoppingcarts": BooleanParamValue.TRUE,
            }
        },

        SMSKeywordEnum.FOOD: {

        },

        SMSKeywordEnum.WATER: {

        },

        SMSKeywordEnum.WIFI: {

        },

        SMSKeywordEnum.TOILET: {

        },
    }

    @classmethod
    def get_param_mappings(cls, sms_keyword_enum:SMSKeywordEnum) -> dict[ParamKeyEnum, dict[str, Any]]:
        try:
            return cls.MAPPING[sms_keyword_enum]
        except KeyError:
            msg = f"`{cls.__name__}` could not find SMSKeywordEnum for input: `{sms_keyword_enum}`"
            logger.error(msg)
            raise ParamResolutionError(msg)        

    @classmethod
    def resolve_params(cls, msg:str, sms_keyword_enum:SMSKeywordEnum) -> ParamDict:
        params = {}
        param_mappings = cls.get_param_mappings(sms_keyword_enum=sms_keyword_enum)
        word_list = cls._tokenize_msg(msg=msg)
        for word in word_list:
            for param_enum, param_keyword_mapping in param_mappings.items():
                if param_keyword_mapping.get(word) is not None:
                    try:
                        resolved_value = param_keyword_mapping[word]
                    except KeyError:
                        msg = f"Could not resolve `{word}` into Param keyword mapping. Keyword enum: `{sms_keyword_enum}`."
                        logger.error(msg)
                        raise ParamResolutionError(msg)
                    else:
                        params[param_enum] = resolved_value if not isinstance(resolved_value, StreetNinjaEnum) else resolved_value.value
                        continue
        return ParamDict(params={**params})


