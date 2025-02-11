from typing import Any
from resources.enums import ShelterCategoryParamValue
from sms.enums import SMSKeywordEnum
from .base_response_templates import ResourceResponseTemplate
from resources.enums import ShelterParamKey
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)

class ShelterResponseTemplate(ResourceResponseTemplate):

    TITLE = "🏠 SHELTERS"

    def _category(self, instance: Shelter) -> str:
        return "All genders" if instance.category == ShelterCategoryParamValue.ADULTS.value else instance.category.capitalize()

    def format_result(self, instance: Shelter) -> str:
        # return instance.facility
        distance = self.distance(km=instance.distance.km)
        s = f"{distance} {instance.facility} ({self._category(instance)})"
        if self.params and self.params.get('category'):
            self.params.pop('category')
        if self.params:
            params_string = self._params_string()
            print(params_string)
            s = f"{s} {params_string}"
        return s


class FoodResponseTemplate(ResourceResponseTemplate):
    
    TITLE = "🍽 FOOD PROGRAMS"

    def format_result(self, instance: FoodProgram) -> str:
        return instance.program_name



class ToiletResponseTemplate(ResourceResponseTemplate):

    keyword_enum = SMSKeywordEnum.TOILET
    TITLE = "🧻 PUBLIC TOILETS"

    def format_result(self, instance: Toilet) -> str:
        return instance.name

class WaterResponseTemplate(ResourceResponseTemplate):

    keyword_enum = SMSKeywordEnum.WATER
    TITLE = "💧 DRINKING FOUNTAINS"

    def format_result(self, instance: DrinkingFountain) -> str:
        ...

class WifiResponseTemplate(ResourceResponseTemplate):

    keyword_enum = SMSKeywordEnum.WIFI
    TITLE = "📶 PUBLIC WIFI"

    def format_result(self, instance: PublicWifi) -> str:
        ...