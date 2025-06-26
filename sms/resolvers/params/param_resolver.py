from dataclasses import dataclass, field
import logging
from typing import Any, Optional
from common.base_enum import StreetNinjaEnum
from sms.enums import SMSKeywordEnum
from .enums import (
    ParamKeyEnum,
    ParamValueEnum,
)
from ..exc import ParamResolutionError
from ..base_resolver import BaseKeywordResolver
from .param_mappings import PARAM_MAPPING
from ..text_normalizer import TextNormalizer


logger = logging.getLogger(__name__)


@dataclass
class ParamDict:
    params: Optional[dict[ParamKeyEnum, ParamValueEnum]] = field(default=None)

    def to_dict(self) -> dict[str, Any]:
        if not self.params:
            return {}
        return {
            k.value if isinstance(k, StreetNinjaEnum) else k:
            v.value if isinstance(v, StreetNinjaEnum) else v
            for k, v in self.params.items()
        }


    # def to_dict(self) -> dict[str, Any]:
    #     return { k.value: v for k, v in self.params.items()} if self.params else {}


class ParamResolver(BaseKeywordResolver):

    MAPPING = PARAM_MAPPING

    @classmethod
    def resolve_params(cls, msg: str, sms_keyword_enum: SMSKeywordEnum) -> ParamDict:
        try:
            param_result = {}
            normalizer = TextNormalizer(keep_ampersand=False, keep_dash=False)
            tokens = normalizer.tokenize_text(msg)
            reverse_map: dict[ParamKeyEnum, dict[str, ParamValueEnum]] = cls.MAPPING.get(sms_keyword_enum, {})

            for param_key, keyword_mapping in reverse_map.items():
                for token in tokens:
                    if token in keyword_mapping and param_key not in param_result:
                        param_result[param_key] = keyword_mapping[token]
        except Exception as e:
            msg = f"ParamResolutionError raised as result of `{e.__class__.__name__}`"
            logger.error(msg, exc_info=True)
            raise ParamResolutionError(msg) from e
        else:
            logger.info(f"Params found: {param_result}")
            return ParamDict(params={**param_result})



#     @classmethod
#     def resolve_params(cls, msg:str, sms_keyword_enum:SMSKeywordEnum) -> ParamDict:
#         params = {}
#         param_mappings = cls.get_param_mappings(sms_keyword_enum=sms_keyword_enum)
#         word_list = cls._tokenize_msg(msg=msg)
#         for word in word_list:
#             for param_enum, param_keyword_mapping in param_mappings.items():
#                 if param_keyword_mapping.get(word) is not None:
#                     try:
#                         resolved_value = param_keyword_mapping[word]
#                     except KeyError:
#                         msg = f"Could not resolve `{word}` into Param keyword mapping. Keyword enum: `{sms_keyword_enum}`."
#                         logger.error(msg)
#                         raise ParamResolutionError(msg)
#                     else:
#                         params[param_enum] = resolved_value if not isinstance(resolved_value, StreetNinjaEnum) else resolved_value.value
#                         continue
#         return ParamDict(params={**params})



















# from dataclasses import dataclass
# import logging
# from typing import Any
# from common.base_enum import StreetNinjaEnum
# from sms.enums import SMSKeywordEnum
# from resources.enums import (
#     ParamKeyEnum,
#     ParamValueEnum,
#     ShelterCategoryParamValue, 
#     ShelterParamKey,
#     BooleanParamValue,
# )
# from .mapping import PARAM_MAPPING
# from ..exc import ParamResolutionError
# from ..base_resolver import BaseKeywordResolver


# logger = logging.getLogger(__name__)


# @dataclass
# class ParamDict:
#     params: dict[ParamKeyEnum, ParamValueEnum] = None

#     def to_dict(self) -> dict[str, Any]:
#         return { k.value: v for k, v in self.params.items()} if self.params else {}


# class ParamResolver(BaseKeywordResolver):
    
#     MAPPING = PARAM_MAPPING

#     @classmethod
#     def get_param_mappings(cls, sms_keyword_enum:SMSKeywordEnum) -> dict[ParamKeyEnum, dict[str, Any]]:
#         try:
#             return cls.MAPPING[sms_keyword_enum]
#         except KeyError:
#             msg = f"`{cls.__name__}` could not find SMSKeywordEnum for input: `{sms_keyword_enum}`"
#             logger.error(msg)
#             raise ParamResolutionError(msg)        

#     @classmethod
#     def resolve_params(cls, msg:str, sms_keyword_enum:SMSKeywordEnum) -> ParamDict:
#         params = {}
#         param_mappings = cls.get_param_mappings(sms_keyword_enum=sms_keyword_enum)
#         word_list = cls._tokenize_msg(msg=msg)
#         for word in word_list:
#             for param_enum, param_keyword_mapping in param_mappings.items():
#                 if param_keyword_mapping.get(word) is not None:
#                     try:
#                         resolved_value = param_keyword_mapping[word]
#                     except KeyError:
#                         msg = f"Could not resolve `{word}` into Param keyword mapping. Keyword enum: `{sms_keyword_enum}`."
#                         logger.error(msg)
#                         raise ParamResolutionError(msg)
#                     else:
#                         params[param_enum] = resolved_value if not isinstance(resolved_value, StreetNinjaEnum) else resolved_value.value
#                         continue
#         return ParamDict(params={**params})


