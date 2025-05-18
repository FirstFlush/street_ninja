from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import LocationType


class Location(gis_models.Model):

    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    location_text = models.CharField(max_length=255, unique=True)
    location = gis_models.PointField(srid=4326)
    date_last = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.location_text}, {LocationType(self.location_type)}"


class Neighborhood(gis_models.Model):

    name = models.CharField(max_length=256)
    boundary = gis_models.PolygonField(srid=4326)
    centroid = gis_models.PointField(srid=4326)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
