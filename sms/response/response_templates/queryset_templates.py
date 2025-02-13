from typing import Any
from resources.enums import ShelterCategoryParamValue
from sms.enums import SMSKeywordEnum
from .base_response_templates import QuerySetResponseTemplate
from resources.enums import ShelterParamKey
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)


class ShelterResponseTemplate(QuerySetResponseTemplate):

    TITLE = "🏠 SHELTERS"

    def _category(self, instance: Shelter) -> str:
        match instance.category:
            case ShelterCategoryParamValue.ADULTS.value:
                category = "All genders"
            case ShelterCategoryParamValue.YOUTH.value:
                category = "Youth - all genders"
            case _:
                category = instance.category
        return category.capitalize()


        

    def format_result(self, instance: Shelter) -> str:
        distance = self.distance(km=instance.distance.km)
        s = f"{distance} {instance.facility} ({self._category(instance)})"
        print('top', self.params)
        if self.params and self.params.get('category'):
            self.params.pop('category')
        print('-------=======-------')
        print(self.params)
        if self.params:
            params_string = self._params_string()
            # print(params_string)
            s = f"{s} {params_string}"
        return s


class FoodResponseTemplate(QuerySetResponseTemplate):

    TITLE = "🍽 FOOD PROGRAMS"

    def format_result(self, instance: FoodProgram) -> str:
        distance = self.distance(km=instance.distance.km)
        s = f"{distance} {instance.program_name}"
        meals = f"Meals: {self._convert_bool(instance.provides_meals)}"
        signup = f"Signup required: {self._convert_bool(instance.signup_required)}"            
        meal_cost = f"Cost: {instance.meal_cost}" if instance.meal_cost else "Free"
        return f"{s} -> {meals} {signup} {meal_cost}"


class ToiletResponseTemplate(QuerySetResponseTemplate):

    keyword_enum = SMSKeywordEnum.TOILET
    TITLE = "🧻 PUBLIC TOILETS"

    def format_result(self, instance: Toilet) -> str:
        distance = self.distance(km=instance.distance.km)
        s = f"{distance} {instance.name} {instance.address}"
        return s


class WaterResponseTemplate(QuerySetResponseTemplate):

    keyword_enum = SMSKeywordEnum.WATER
    TITLE = "💧 DRINKING FOUNTAINS"

    def format_result(self, instance: DrinkingFountain) -> str:
        distance = self.distance(km=instance.distance.km)
        s = f"{distance} {instance.name} {instance.in_operation}"
        return s

class WifiResponseTemplate(QuerySetResponseTemplate):

    keyword_enum = SMSKeywordEnum.WIFI
    TITLE = "📶 PUBLIC WIFI"

    def format_result(self, instance: PublicWifi) -> str:
        distance = self.distance(km=instance.distance.km)
        s = f"{distance} {instance.ssid}"
        return s