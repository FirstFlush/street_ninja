from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import LocationType


class Location(gis_models.Model):

    total_inquiries = models.IntegerField(default=0)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    location_text = models.CharField(max_length=255)
    location = gis_models.PointField(srid=4326)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.location_text}, {LocationType(self.location_type)}"
