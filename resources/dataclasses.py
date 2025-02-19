from dataclasses import dataclass
from typing import Literal, Any


@dataclass
class MapPoint:
    longitude: float
    latitude: float
    key:int
    data: dict[str, Any]


@dataclass
class MapData:
    resources: dict[Literal["shelter", "food", "water", "toilet", "wifi"], list[MapPoint]]
    


