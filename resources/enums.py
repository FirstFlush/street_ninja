from common.enums import StreetNinjaEnum


class ParamEnum(StreetNinjaEnum):
    """Abstract parent for all enums related to SMS inquiry params."""
    pass


class ParamKeyEnum(ParamEnum):
    """Defines the keys used for filtering."""

    @classmethod
    def values_response(cls, *exclude: str) -> list[str]:
        """This method is to help format sms responses"""
        return [value for value in cls.values if value not in exclude]
        

class ParamValueEnum(ParamEnum):
    """Defines the possible values for filtering parameters."""
    pass


class ShelterParamKey(ParamKeyEnum):
    CATEGORY = "category"
    PETS = "pets"
    CARTS = "carts"


class ShelterCategoryParamValue(ParamValueEnum):
    MEN = "Men"
    ADULTS = "Adults (all genders)"
    WOMEN = "Women"
    YOUTH = "Youth (all genders)"


class BooleanParamValue(ParamValueEnum):
    TRUE = True
    FALSE = False