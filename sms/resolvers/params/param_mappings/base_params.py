from abc import ABC
from ..enums import ParamKeyEnum, ParamValueEnum
from sms.resolvers.text_normalizer import TextNormalizer

class BaseResourceParams(ABC):

    PARAM_MAPPING: dict[ParamKeyEnum, dict[ParamValueEnum, list[str]]] | None = None

    @classmethod
    def reverse_mapping(cls) -> dict[ParamKeyEnum, dict[str, ParamValueEnum]]:
        d = {}
        normalizer = TextNormalizer(keep_ampersand=False, keep_dash=False)
        for param_key, param_values_dict in cls.PARAM_MAPPING.items():
            d[param_key] = {}
            for param_value, values in param_values_dict.items():
                for value in normalizer.tokenize_list(values):
                    d[param_key][value] = param_value
        return d