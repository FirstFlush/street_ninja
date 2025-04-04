from .base_params import BaseResourceParams
from ..enums import ParamKeyEnum, ParamValueEnum, BooleanParamValue


class FoodParamKey(ParamKeyEnum):
    MEALS = "provides_meals"
    HAMPERS = "provides_hampers"
    WHEELCHAIR = "wheelchair_accessible"
    TAKEOUT = "takeout_available"
    DELIVER = "delivery_available"


class FoodParams(BaseResourceParams):

    PARAM_MAPPING = {
        FoodParamKey.MEALS: {
            BooleanParamValue.TRUE: [
                "meal", "meals",
            ]
        },
        FoodParamKey.HAMPERS: {
            BooleanParamValue.TRUE: [
                "hamper", "hampers", "groceries", "grocery",
            ]
        },
        FoodParamKey.WHEELCHAIR: {
            BooleanParamValue.TRUE: [
                "wheelchair", "wheelchairs",
            ]
        },
        FoodParamKey.TAKEOUT: {
            BooleanParamValue.TRUE: [
                "takeout", "takeaway",
            ]
        },
        FoodParamKey.DELIVER: {
            BooleanParamValue.TRUE: [
                "delivery", "deliver", "homedelivery",
            ]
        }
    }
