from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import LocationType
from typing import Any


class Location(gis_models.Model):

    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    location_text = models.CharField(max_length=255, unique=True)
    location = gis_models.PointField(srid=4326)
    date_last = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.location_text}, {LocationType(self.location_type)}"


class NeighborhoodManager(models.Manager):

    def cache_data(self) -> list[dict[str, Any]]:
        """
        Returns Neighborhood objects as a list of dicts with only relevant information

        Example:
        [
          {
            "name": "Kitsilano",
            "centroid": Point(),
          }, 
          ...etc
        ]
        """
        return list(self.get_queryset().all().values("name", "centroid"))


class Neighborhood(gis_models.Model):

    name = models.CharField(max_length=256)
    boundary = gis_models.PolygonField(srid=4326)
    centroid = gis_models.PointField(srid=4326)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects:NeighborhoodManager = NeighborhoodManager()
