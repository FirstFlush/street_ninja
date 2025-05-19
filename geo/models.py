from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import LocationType
from .neighborhoods.dataclasses import NeighborhoodCacheData
from sms.resolvers.text_normalizer import TextNormalizer


class Location(gis_models.Model):

    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    location_text = models.CharField(max_length=255, unique=True)
    location = gis_models.PointField(srid=4326)
    date_last = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.location_text}, {LocationType(self.location_type)}"


class NeighborhoodManager(models.Manager):

    def cache_data(self) -> list[NeighborhoodCacheData]:
        """
        Returns Neighborhood objects as a list of dicts with only relevant information.

        Each entry includes:
          - name
          - name_normalized
          - centroid
        """
        normalizer = TextNormalizer()
        raw_data = self.get_queryset().values("name", "centroid")

        result = []
        for d in raw_data:
            name_normalized = normalizer.normalize_text(text=d["name"], strip_spaces=True)
            result.append(NeighborhoodCacheData(**{
                **d,
                "name_normalized": name_normalized,
            }))

        return result

class Neighborhood(gis_models.Model):

    name = models.CharField(max_length=256)
    boundary = gis_models.PolygonField(srid=4326)
    centroid = gis_models.PointField(srid=4326)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    objects:NeighborhoodManager = NeighborhoodManager()

    def __str__(self) -> str:
        return self.name