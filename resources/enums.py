from common.enums import StreetNinjaEnum


class ShelterCategoryEnum(StreetNinjaEnum):

    MEN = "Men"
    ADULTS = "Adults (all genders)"
    WOMEN = "Women"
    YOUTH = "Youth (all genders)"


class ParamEnum(StreetNinjaEnum):
    """"""
    pass

class ShelterParamEnum(ParamEnum):

    CATEGORY = "category"
    PETS = "pets"
    CARTS = "carts"