from enum import Enum, EnumMeta
from typing import Any


class StreetNinjaEnumMeta(EnumMeta):

    @property
    def choices(cls) -> list[tuple[Any, str]]:
        """Returns a list of tuples that can be used in models.CharField's choices property.
        Example:
            [
                ("red", "Red"),
                ("blue", "Blue"),
            ]
        """
        return [(enum.value, enum.name.replace('_',' ').title()) for enum in cls]

    @property
    def values(cls) -> list[Any]:
        return [enum.value for _, enum in cls.__members__.items()]


class StreetNinjaEnum(Enum, metaclass=StreetNinjaEnumMeta):
    pass