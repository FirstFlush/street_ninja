import logging
from django.contrib.gis.geos import Point
from collections import defaultdict
from sms.enums import SMSKeywordEnum
from .abstract_models import ResourceModel
from .dataclasses import MapData, MapPoint
from .models import Shelter, FoodProgram, DrinkingFountain, Toilet, PublicWifi


logger = logging.getLogger(__name__)


class ResourceService:
    RESOURCE_MODELS: dict[SMSKeywordEnum, ResourceModel] = {
        SMSKeywordEnum.FOOD: FoodProgram,
        SMSKeywordEnum.SHELTER: Shelter,
        SMSKeywordEnum.WATER: DrinkingFountain,
        SMSKeywordEnum.WIFI: PublicWifi,
        SMSKeywordEnum.TOILET: Toilet,
    }

    def build_map_data(self) -> MapData | None:
        """  
        Constructs a MapData object containing categorized geospatial resource points.

        This method retrieves active resource records from the database, extracts their 
        geographical locations, and organizes them into a structured format suitable 
        for API responses and map rendering.        
        """
        map_data = defaultdict(list)

        count = 0
        for keyword_enum, model_class in self.RESOURCE_MODELS.items():
            qs = model_class.objects.filter(is_active=True)#.map_values("location")
            for obj in qs:
                if obj.location:
                    count += 1
                    map_point = MapPoint(
                        longitude=obj.location.x,
                        latitude=obj.location.y,
                        key=count,
                        data=obj.map_values,
                        # name=obj.get("facility"),
                    )
                    map_data[keyword_enum.value.lower()].append(map_point)
        if len(map_data.keys()) == 0:
            logger.warning(f"`{len(map_data.keys())}` resource records found when building MapData")
            return None

        return MapData(resources=dict(map_data))
