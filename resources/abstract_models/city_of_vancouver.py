from typing import Any
from django.contrib.gis.geos import Point
from .base_model import ResourceModel


class CityOfVancouverModel(ResourceModel):
    
    class Meta:
        abstract = True

    @classmethod
    def normalize_data(cls, data:dict[str, Any]) -> dict[str, Any]:
        data['location'] = cls.get_location(data)
        data.pop('geo_point_2d')
        return data

    @classmethod
    def get_location(cls, data:dict[str, Any]) -> Point:
        return cls.get_point(lon=data['geo_point_2d']['lon'], lat=data['geo_point_2d']['lat'])
