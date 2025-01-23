import logging
from typing import Any
from common.enums import SMSKeywordEnum, LanguageEnum, StreetNinjaEnum
from resources.enums import (
    ParamEnum,
    ShelterCategoryEnum, 
    ShelterParamEnum,
)
from ..exc import KeywordResolverError
from .base_resolver import BaseKeywordResolver


logger = logging.getLogger(__name__)


class KeywordParamResolver(BaseKeywordResolver):
    
    MAPPING = {
        SMSKeywordEnum.SHELTER: {
            ShelterParamEnum.CATEGORY: {
                "woman": ShelterCategoryEnum.WOMEN,
                "women": ShelterCategoryEnum.WOMEN,
                "womens": ShelterCategoryEnum.WOMEN,
                "ladies": ShelterCategoryEnum.WOMEN,
                "female": ShelterCategoryEnum.WOMEN,
                "females": ShelterCategoryEnum.WOMEN,
                "man": ShelterCategoryEnum.MEN,
                "men": ShelterCategoryEnum.MEN,
                "mens": ShelterCategoryEnum.MEN,
                "male": ShelterCategoryEnum.MEN,
                "males": ShelterCategoryEnum.MEN,
                "youth": ShelterCategoryEnum.YOUTH,
                "youths": ShelterCategoryEnum.YOUTH,
                "kid": ShelterCategoryEnum.YOUTH,
                "kids": ShelterCategoryEnum.YOUTH,                
                "teen": ShelterCategoryEnum.YOUTH,
                "teens": ShelterCategoryEnum.YOUTH,
                "teenager": ShelterCategoryEnum.YOUTH,
                "teenagers": ShelterCategoryEnum.YOUTH,
                "adult": ShelterCategoryEnum.ADULTS,
                "adults": ShelterCategoryEnum.ADULTS,
            },
            ShelterParamEnum.PETS: {
                # "allergy": False,
                # "allergic": False,
                # "petallergy": False,
                "pet": True,
                "pets": True,
                "dog": True,
                "dogs": True,
                "cat": True,
                "cats": True,
                "animal": True,
                "animals": True,
                "petfriendly": True,
            },
            ShelterParamEnum.CARTS: {
                "cart": True,
                "carts": True,
                "shoppingcart": True,
                "shoppingcarts": True,
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
    def get_param_mappings(cls, sms_keyword_enum:SMSKeywordEnum) -> dict[ParamEnum, dict[str, Any]]:
        try:
            return cls.MAPPING[sms_keyword_enum]
        except KeyError:
            msg = f"`{cls.__name__}` could not find SMSKeywordEnum for input: `{sms_keyword_enum}`"
            logger.error(msg)
            raise KeywordResolverError(msg)        

    @classmethod
    def resolve_params(cls, msg:str, sms_keyword_enum:SMSKeywordEnum) -> dict[str, Any]:
        params = {}
        param_mappings = cls.get_param_mappings(sms_keyword_enum=sms_keyword_enum)
        word_list = cls._prepare_words(msg=msg)
        for word in word_list:
            for param_enum, param_keyword_mapping in param_mappings.items():
                if param_keyword_mapping.get(word) is not None:
                    try:
                        resolved_value = param_keyword_mapping[word]
                    except KeyError:
                        msg = f"Could not resolve `{word}` into Param keyword mapping. Keyword enum: `{sms_keyword_enum}`."
                        logger.error(msg)
                        raise KeywordResolverError(msg)
                    else:
                        params[param_enum.value] = resolved_value if not isinstance(resolved_value, StreetNinjaEnum) else resolved_value.value
                        continue
        return params


