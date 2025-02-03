import logging
from typing import Any
from django.contrib.gis.geos import Point
from .base_model import ResourceModel

logger = logging.getLogger(__name__)


class CityOfVancouverModel(ResourceModel):

    class Meta:
        abstract = True

    @classmethod
    def normalize_data(cls, data:dict[str, Any]) -> dict[str, Any]:
        geo_key = cls._get_geo_key(data)
        data['location'] = cls.get_location(data, geo_key=geo_key)
        data.pop(geo_key)
        return data

    @staticmethod
    def _get_geo_key(data: dict[str, Any]) -> str:
        """
        Different endpoints at City Of Vancouver OpenData API have different structures
        for how they store their geometric data.
        """
        keys_to_check = {"geo_point_2d", "geom"}
        for key in keys_to_check & data.keys():
            if key == "geo_point_2d":
                geo_key = "geo_point_2d"
            elif key == "geom":
                geo_key = "geom"
            else:
                logger.error(f"Can not find geometry key from data: `{data}`")
                raise KeyError("Geometry key not found in incoming JSON data. Can not find longitude/latitude.")
        return geo_key

    @classmethod
    def get_location(cls, data:dict[str, Any], geo_key:str) -> Point:
        return cls.get_point(lon=data[geo_key]['lon'], lat=data[geo_key]['lat'])
