from common.enums import StreetNinjaEnum


class ParamEnum(StreetNinjaEnum):
    """Abstract parent for all enums related to SMS inquiry params."""
    pass


class ParamKeyEnum(ParamEnum):
    """
    Defines the keys used in the resource filter query's kwargs dict    
    example: Model.object.filter(**kwargs)
    """

    @classmethod
    def values_response(cls, *exclude: str) -> list[str]:
        """This method is to help format sms responses"""
        return [value for value in cls.values if value not in exclude]
        

class ParamValueEnum(ParamEnum):
    """Defines the possible values for filtering parameters."""
    pass


class BooleanParamValue(ParamValueEnum):
    TRUE = True
    FALSE = False


# class ShelterParamKey(ParamKeyEnum):
#     CATEGORY = "category"
#     PETS = "pets"
#     CARTS = "carts"


# class ShelterCategoryParamValue(ParamValueEnum):
#     MEN = "Men"
#     ADULTS = "Adults (all genders)"
#     WOMEN = "Women"
#     YOUTH = "Youth (all genders)"



# class FoodParamKey(ParamKeyEnum):
#     MEALS = "meals"
#     HAMPERS = "hampers"
#     WHEELCHAIR = "wheelchair_accessible"
#     TAKEOUT = "takeout_available"
#     DELIVER = "delivery_available"
