from django.contrib.gis.geos import Point
from .base_model import ResourceModel


class WigleModel(ResourceModel):
    

    class Meta:
        abstract = True

    @classmethod
    def get_location(cls, data:dict[str, float]) -> Point:
        return cls.get_point(lon=data['trilong'], lat=['trilat'])