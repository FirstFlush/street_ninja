from .base_params import BaseResourceParams
from ..enums import ParamKeyEnum, ParamValueEnum, BooleanParamValue 


class ShelterParamKey(ParamKeyEnum):
    CATEGORY = "category"
    PETS = "pets"
    CARTS = "carts"


class ShelterCategoryParamValue(ParamValueEnum):
    MEN = "Men"
    ADULTS = "Adults (all genders)"
    WOMEN = "Women"
    YOUTH = "Youth (all genders)"


class ShelterParams(BaseResourceParams):

    PARAM_MAPPING = {
        ShelterParamKey.CATEGORY: {
            ShelterCategoryParamValue.WOMEN: [
                "woman", "women", "womens", "womans", "lady", "ladies", "female", "females",
            ],
            ShelterCategoryParamValue.MEN: [
                "man", "men", "mens", "male", "males", "gentleman", "gentlemen",
            ],
            ShelterCategoryParamValue.ADULTS: [
                "adult", "adults", "everyone", "everybody",
            ],
            ShelterCategoryParamValue.YOUTH: [
                "youth", "youths", "kid", "kids", "teen", "teens", "teenager", "teenagers"
            ],
        },
        ShelterParamKey.PETS: {
            BooleanParamValue.TRUE: [
                "pet", "pets", "petfriendly", "dog", "dogs", "cat", "cats", "animal", "animals"
            ],
        },
        ShelterParamKey.CARTS: {
            BooleanParamValue.TRUE: [
                "cart", "carts", "shoppingcart", "shoppingcarts"
            ],
        },

    }
