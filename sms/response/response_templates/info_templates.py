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

    def __init__(self, instance: T):
        self.instance = instance

    @abstractmethod
    def display_info(self) -> str:
        ...


class ShelterInfoTemplate(InfoTemplate[Shelter]):
    
    def _address(self) -> str:
        if self.instance.address:
            return self.instance.address
        else:
            return "(Address not listed)"

    def display_info(self) -> str:
        return f"""
{self.instance.facility}
{self.instance.category}

{self._address()}
{self.instance.phone}

Serves meals: {self._convert_bool(self.instance.meals)}
Pets allowed: {self._convert_bool(self.instance.pets)}
Carts allowed: {self._convert_bool(self.instance.carts)}
"""


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
        return f"{s}\nCost: {self.instance.hamper_cost}"

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

    def _pet_friendly(self) -> str:
        if self.instance.pet_friendly is not None:
            return f"\nPet-friendly: {self._convert_bool(self.instance.pet_friendly, allow_null=True)}"
        return ""

    def display_info(self) -> str:
        return f"""
{self.instance.name}

In operation: {self.instance.in_operation}
{self._pet_friendly()}
"""


class ToiletInfoTemplate(InfoTemplate[Toilet]):

    def _address(self) -> str:
        return self.instance.address if self.instance.address \
            else "(Address not listed)" 

    def _details(self) -> str:
        details = []
        if self.instance.description:
            details.append(self.instance.description)
        if self.instance.notes:
            details.append(self.instance.notes)
        return "\n".join(details) if details else "(No details)"

    def _hours(self) -> str:
        summer_hours = self.instance.summer_hours if self.instance.summer_hours else "Unknown"
        winter_hours = self.instance.winter_hours if self.instance.winter_hours else "Unknown"
        return f"Summer hours: {summer_hours}\nWinter hours: {winter_hours}"


    def display_info(self) -> str:
        return f"""
{self.instance.name}

{self.instance.address}

{self._details()}

{self._hours()}

Wheelchair accessible: {self._convert_bool(self.instance.is_wheelchair)}
"""


class WifiInfoTemplate(InfoTemplate[PublicWifi]):

    def _name(self) -> str:
        if self.instance.name:
            return f"{self.instance.name}\n"
        return ""

    def _address(self) -> str:
        if self.instance.address:
            return f"{self.instance.address}\n"
        return ""

    def display_info(self) -> str:

        return f"""
{self._name()}
{self._address()}
SSID: {self.instance.ssid}

"""


