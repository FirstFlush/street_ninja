from abc import abstractmethod
from typing import Generic, TypeVar
from .base_response_templates import GeneralResponseTemplate
from resources.abstract_models import ResourceModel
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)

T = TypeVar('T', bound=ResourceModel)

class InfoTemplate(GeneralResponseTemplate, Generic[T]):

    def __init__(self, instance: T) -> str:
        self.instance = instance

    @abstractmethod
    def display_info(self, instance: ResourceModel) -> str:
        ...


class ShelterInfoTemplate(InfoTemplate[Shelter]):
    
    def display_info(self) -> str:
        return f"{self.instance.facility} blehhh"



class FoodInfoTemplate(InfoTemplate[FoodProgram]):

    def _meals(self) -> str:
        s = f"Meals: {self._convert_bool(self.instance.provides_meals)}"
        if not self.instance.meal_cost:
            return s
        return f"{s}\nCost: {self.instance.meal_cost}"

    def _hampers(self) -> str:
        s = f"Hampers: {self._convert_bool(self.instance.provides_hampers)}"
        if not self.instance.hamper_cost:
            return s
        return f"Cost: {self.instance.hamper_cost}"

    def _address(self) -> str:
        addy = self.instance.location_address if self.instance.location_address else "(no address provided)"
        return f"{addy}\n{self.instance.address_extra_info}" if self.instance.address_extra_info else addy

    def _signup(self) -> str:
        if not self.instance.signup_required:
            return f"Sign-up required: {self._convert_bool(self.instance.signup_required)}"
        s = f"Sign-up required: {self._convert_bool(self.instance.signup_required)}"
        if self.instance.signup_phone_number:
            s += f"\n{self.instance.signup_phone_number}"
        if self.instance.signup_email:
            s += f"\n{self.instance.signup_email}"
        return s

    def _referral(self) -> str:
        if not self.instance.requires_referral:
            return f"Referral required: {self._convert_bool(self.instance.requires_referral)}"
        else:
            s = f"Referral required: {self._convert_bool(self.instance.requires_referral)}"
        if self.instance.referral_agency_name:
            s += f"\nReferral agency: {self.instance.referral_agency_name}"
        if self.instance.referral_phone_number:
            s += f"\n{self.instance.referral_phone_number}"
        if self.instance.referral_email:
            s += f"\n{self.instance.referral_email}"
        return s


    def _program(self) -> str:
        if self.instance.program_population_served:
            return f"{self.instance.program_name}\nPopulation served: {self.instance.program_population_served}"
        return self.instance.program_name


    def display_info(self) -> str:
        return f"""
{self._program()}

{self._address()}

{self.instance.description}

{self._signup()}

{self._referral()}

{self._meals()}

{self._hampers()}

Delivery: {self._convert_bool(self.instance.delivery_available)}
Takeout: {self._convert_bool(self.instance.takeout_available)}
Wheelchair Access: {self._convert_bool(self.instance.wheelchair_accessible)}

Organized by
{self.instance.organization_name}
""" 

class WaterInfoTemplate(InfoTemplate[DrinkingFountain]):

    def display_info(self) -> str:
        ...


class ToiletInfoTemplate(InfoTemplate[Toilet]):

    def display_info(self) -> str:
        ...


class WifiInfoTemplate(InfoTemplate[PublicWifi]):

    def display_info(self) -> str:
        ...


