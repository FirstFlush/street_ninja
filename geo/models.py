from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import LocationType


class Location(gis_models.Model):

    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    location_text = models.CharField(max_length=255, unique=True)
    location = gis_models.PointField(srid=4326)
    date_last = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def count_hits(self) -> int:
        return self.inquirycount_set.count()

    def __str__(self) -> str:
        return f"{self.location_text}, {LocationType(self.location_type)}"


class InquiryCount(models.Model):

    location = models.ForeignKey(to=Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

