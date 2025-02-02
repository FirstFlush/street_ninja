from dataclasses import dataclass, asdict
from typing import Literal, Optional

@dataclass
class MapPoint:
    # type: Literal["shelter", "food", "water", "toilet", "wifi"]
    longitude: float
    latitude: float
    key:int
    # name: Optional[str] = None


@dataclass
class MapData:
    data: dict[Literal["shelter", "food", "water", "toilet", "wifi"], list[MapPoint]]
    


