"""
Global mappings for the app.

This file centralizes mappings that connect keywords, services, response templates, etc.
If something needs to be linked across the app (like a new resource type), this is
probably where it goes. 
"""
from cache.redis.access_patterns.resources import (
    ShelterAccessPattern,
    FoodProgramAccessPattern,
    ToiletAccessPattern,
    DrinkingFountainAccessPattern,
    PublicWifiAccessPattern,
    AccessPatternDB
)
from geo.enums import GeocoderEnum
from geo.geocoding.geocoders import NominatimGeocoder, OpenCageGeocoder
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceModel
from resources.models import (
    Shelter,
    FoodProgram,
    Toilet,
    DrinkingFountain,
    PublicWifi,
)
from sms.response.response_templates import (
    ShelterResponseTemplate,
    FoodResponseTemplate,
    ToiletResponseTemplate,
    WaterResponseTemplate,
    WifiResponseTemplate,
)
from sms.response.response_templates.info_templates import (
    InfoTemplate,
    ShelterInfoTemplate,
    FoodInfoTemplate,
    WaterInfoTemplate,
    ToiletInfoTemplate,
    WifiInfoTemplate,
)


# SMS_KEYWORD_ENUM_TO_RESOURCE_MODEL = {
#     SMSKeywordEnum.SHELTER: Shelter,
#     SMSKeywordEnum.FOOD: FoodProgram,
#     SMSKeywordEnum.TOILET: Toilet,
#     SMSKeywordEnum.WATER: DrinkingFountain,
#     SMSKeywordEnum.WIFI: PublicWifi,
# }


ACCESS_PATTERN_TO_MODEL: dict[AccessPatternDB, ResourceModel] = {
        FoodProgramAccessPattern: FoodProgram,
        ShelterAccessPattern: Shelter,
        DrinkingFountainAccessPattern: DrinkingFountain,
        ToiletAccessPattern: Toilet,
        PublicWifiAccessPattern: PublicWifi,
    }

SMS_KEYWORD_ENUM_TO_RESPONSE_TEMPLATE = {
    SMSKeywordEnum.SHELTER: ShelterResponseTemplate,
    SMSKeywordEnum.FOOD: FoodResponseTemplate,
    SMSKeywordEnum.TOILET: ToiletResponseTemplate,
    SMSKeywordEnum.WATER: WaterResponseTemplate,
    SMSKeywordEnum.WIFI: WifiResponseTemplate,
}

SMS_KEYWORD_ENUM_TO_ACCESS_PATTERN = {
    SMSKeywordEnum.FOOD: FoodProgramAccessPattern,
    SMSKeywordEnum.SHELTER: ShelterAccessPattern,
    SMSKeywordEnum.WATER: DrinkingFountainAccessPattern,
    SMSKeywordEnum.TOILET: ToiletAccessPattern,
    SMSKeywordEnum.WIFI: PublicWifiAccessPattern,
}


GEOCODER_ENUM_TO_GEOCODER = {
    GeocoderEnum.OPENCAGE : OpenCageGeocoder,
    GeocoderEnum.NOMINATIM : NominatimGeocoder,
}


SMS_KEYWORD_ENUM_TO_INFO_TEMPLATE: dict[SMSKeywordEnum, InfoTemplate] = {
    SMSKeywordEnum.SHELTER : ShelterInfoTemplate,
    SMSKeywordEnum.FOOD : FoodInfoTemplate,
    SMSKeywordEnum.WATER : WaterInfoTemplate,
    SMSKeywordEnum.TOILET : ToiletInfoTemplate,
    SMSKeywordEnum.WIFI : WifiInfoTemplate,
}


