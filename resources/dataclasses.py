from dataclasses import dataclass
from typing import Literal, Any


@dataclass
class MapPointData:
    info_template_data: str


@dataclass
class MapPoint:
    longitude: float
    latitude: float
    id: int


@dataclass
class MapData:
    resources: dict[Literal["shelter", "food", "water", "toilet", "wifi"], list[MapPoint]]
    


