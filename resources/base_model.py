from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point


class ResourceQuerySet(gis_models.QuerySet):

    ...


class ResourceManager(gis_models.Manager):

    def get_queryset(self):
        return ResourceQuerySet(self.model, using=self._db)    


class ResourceModel(gis_models.Model):

    objects = ResourceManager.from_queryset(ResourceQuerySet)()

    class Meta:
        abstract = True


    def get_point(self, lon:float, lat:float) -> Point:
        return Point(lon, lat, srid=4326)
    
    def save(self, **kwargs):
        super().save(**kwargs)