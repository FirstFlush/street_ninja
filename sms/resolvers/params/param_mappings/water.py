from .base_params import BaseResourceParams
from ..enums import ParamKeyEnum, ParamValueEnum, BooleanParamValue 


class WaterParamKey(ParamKeyEnum):
    PETS = "pet_friendly"


class WaterParams(BaseResourceParams):

    PARAM_MAPPING = {
        WaterParamKey.PETS : {
            BooleanParamValue.TRUE: [
                'pet', 'pets', 'petfriendly',
            ]
        }
    }
