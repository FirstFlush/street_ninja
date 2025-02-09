from sms.enums import SMSKeywordEnum
from .base_response_templates import ResourceResponseTemplate
from resources.enums import ShelterParamKey


class ShelterResponseTemplate(ResourceResponseTemplate):

    keyword_enum = SMSKeywordEnum.SHELTER
    always_show = ["facility", "category", "address"]
    optional_params = ShelterParamKey.values_response("category")
    response_format = "{facility} - {category} - {address} {extra_params}"


class FoodResponseTemplate(ResourceResponseTemplate):
    
    keyword_enum = SMSKeywordEnum.FOOD
    always_show = ["name", "time"]
    optional_params = ["dietary"]
    response_format = "{name} - {time} {extra_params}"
