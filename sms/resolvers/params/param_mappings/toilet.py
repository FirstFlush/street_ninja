from .base_params import BaseResourceParams
from ..enums import ParamKeyEnum, ParamValueEnum, BooleanParamValue 


class ToiletParamKey(ParamKeyEnum):
    WHEELCHAIR = "is_wheelchair"


class ToiletParams(BaseResourceParams):

    PARAM_MAPPING = {
        ToiletParamKey.WHEELCHAIR: {
            BooleanParamValue.TRUE: [
                'wheelchair', 'wheelchairs', 'wheelchairfriendly', 'handicap', 'handicapped', 
                'disabled', 'disability',
            ]
        }
    }