from sms.enums import SMSKeywordEnum
from .shelter import ShelterParams
from .food import FoodParams
from .toilet import ToiletParams
from .water import WaterParams

PARAM_MAPPING = {
    SMSKeywordEnum.SHELTER : ShelterParams.reverse_mapping(),
    SMSKeywordEnum.FOOD : FoodParams.reverse_mapping(),
    SMSKeywordEnum.TOILET : ToiletParams.reverse_mapping(),
    SMSKeywordEnum.WATER : WaterParams.reverse_mapping(),
    SMSKeywordEnum.WIFI : {},
}