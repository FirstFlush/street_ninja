from django.contrib.gis.db import models as gis_models


class ResourceQuerySet(gis_models.QuerySet):

    ...


class ResourceManager(gis_models.Manager):

    def get_queryset(self):
        return ResourceQuerySet(self.model, using=self._db)    


class ResourceModel(gis_models.Model):

    objects = ResourceManager.from_queryset(ResourceQuerySet)()

    class Meta:
        abstract = True