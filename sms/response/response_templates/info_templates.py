from abc import abstractmethod
from .base_response_templates import GeneralResponseTemplate
from resources.abstract_models import ResourceModel
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)


class InfoTemplate(GeneralResponseTemplate):

    @abstractmethod
    def display_info(self, instance: ResourceModel) -> str:
        ...


class ShelterInfoTemplate(InfoTemplate):
    
    def display_info(self, instance: Shelter) -> str:
        return f"{instance.facility} blehhh"



class FoodInfoTemplate(InfoTemplate):

    def display_info(self, instance: FoodProgram) -> str:
        ...

class WaterInfoTemplate(InfoTemplate):

    def display_info(self, instance: DrinkingFountain) -> str:
        ...


class ToiletInfoTemplate(InfoTemplate):

    def display_info(self, instance: Toilet) -> str:
        ...


class WifiInfoTemplate(InfoTemplate):

    def display_info(self, instance: Shelter) -> str:
        ...


