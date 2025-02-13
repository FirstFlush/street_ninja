from .base_response_templates import BaseSMSResponseTemplate
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)


class InfoTemplate(BaseSMSResponseTemplate):
    ...



class ShelterInfoTemplate(InfoTemplate):
    
    def info(self, instance: Shelter):
        ...



class FoodInfoTemplate(InfoTemplate):
    ...


class WaterInfoTemplate(InfoTemplate):
    ...


class ToiletInfoTemplate(InfoTemplate):
    ...


class WifiInfoTemplate(InfoTemplate):
    ...


