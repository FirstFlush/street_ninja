from abc import abstractmethod
from django.conf import settings
from typing import Any
from resources.enums import ShelterCategoryParamValue
from sms.enums import SMSKeywordEnum
from .base_response_templates import BaseSMSResponseTemplate
from .welcome_template import WelcomeTemplate
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)


class QuerySetResponseTemplate(BaseSMSResponseTemplate):

    keyword_enum: SMSKeywordEnum | None = None
    FOOTER = """
More? 'MORE' | Help? 'HELP'
Details? '# INFO' | Maps? '# DIRECTIONS'
"""

    def __init__(self, params: dict[str, Any] | None = None):
        self.params = params

    @abstractmethod
    def format_result(self) -> str:
        ...

    def _params_string(self, sep: str = ", ") -> str:
        return sep.join([f"{k.capitalize()} {self._convert_bool(v, abbreviated=False) if isinstance(v, bool) else v}" for k, v in self.params.items()])


    def distance(self, km: float) -> str:
        km = f"{round(km,1)}".rstrip("0").rstrip(".")
        return f"{km}km"
    
    def wrap_response(self, msg:str, new_session: bool = False) -> str:
        if new_session:
            top = f"{WelcomeTemplate.welcome_header()}\n\n{self.TITLE}"
            bottom = f"{WelcomeTemplate.WELCOME_FOOTER}"
            wrapped_msg = f"{top}\n{msg}{bottom}"
        else:
            top = self.TITLE
            bottom = f"{self.FOOTER}"
            wrapped_msg = f"{top}\n\n{msg}\n{bottom}"
            if msg == settings.END_OF_RESULTS:

                wrapped_msg = wrapped_msg.replace(bottom, "")
        return wrapped_msg


class ShelterResponseTemplate(QuerySetResponseTemplate):

    TITLE = "SHELTERS"

    def _category(self, instance: Shelter) -> str:
        match instance.category:
            case ShelterCategoryParamValue.ADULTS.value:
                category = "Adults - all genders"
            case ShelterCategoryParamValue.YOUTH.value:
                category = "Youth - all genders"
            case _:
                category = instance.category
        return category.capitalize()        

    def format_result(self, instance: Shelter) -> str:
        distance = self.distance(km=instance.distance)
        s = f"{distance} {instance.facility} ({self._category(instance)})"
        if self.params and self.params.get('category'):
            self.params.pop('category')
        if self.params:
            params_string = self._params_string()
            s = f"{s} {params_string}"
        return s


class FoodResponseTemplate(QuerySetResponseTemplate):

    TITLE = "FOOD PROGRAMS"

    def _signup_or_referral(self, instance:FoodProgram) -> str:
        d = {
            "sign-up required" : instance.signup_required,
            "referral required" : instance.requires_referral,
        }
        txt = ", ".join(txt for txt, is_available in d.items() if is_available).capitalize()
        if txt:
            return f"*{txt}*"
        return ""

    def _program_offerings(self, instance: FoodProgram) -> str:
        offerings = {
            "meals": (instance.provides_meals, instance.meal_cost),
            "hampers": (instance.provides_hampers, instance.hamper_cost),
            "delivery": (instance.delivery_available, None),
            "takeout": (instance.takeout_available, None),
        }

        return ", ".join(
            f"{name} ({cost if cost is not None else 'UNKNOWN'})" 
            if cost is not None or name in ["meals", "hampers"] else name
            for name, (is_available, cost) in offerings.items()
            if is_available
        )

    def format_result(self, instance: FoodProgram) -> str:
        distance = self.distance(km=instance.distance)
        s = f"{distance} {instance.program_name}"
        return f"{s}: {self._program_offerings(instance)} {self._signup_or_referral(instance)}"


class ToiletResponseTemplate(QuerySetResponseTemplate):

    keyword_enum = SMSKeywordEnum.TOILET
    TITLE = "TOILETS"

    def format_result(self, instance: Toilet) -> str:
        distance = self.distance(km=instance.distance)
        s = f"{distance} {instance.name} {instance.address}"
        return s


class WaterResponseTemplate(QuerySetResponseTemplate):

    keyword_enum = SMSKeywordEnum.WATER
    TITLE = "FOUNTAINS"

    def format_result(self, instance: DrinkingFountain) -> str:
        distance = self.distance(km=instance.distance)
        s = f"{distance} {instance.name} {instance.in_operation}"
        return s


class WifiResponseTemplate(QuerySetResponseTemplate):

    keyword_enum = SMSKeywordEnum.WIFI
    TITLE = "PUBLIC WIFI"

    def format_result(self, instance: PublicWifi) -> str:
        distance = self.distance(km=instance.distance)
        s = f"{distance} {instance.ssid}"
        return s