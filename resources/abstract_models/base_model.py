import logging
from typing import Any
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point


logger = logging.getLogger(__name__)


class ResourceQuerySet(gis_models.QuerySet):
    ...


class ResourceManager(gis_models.Manager):

    def get_queryset(self):
        return ResourceQuerySet(self.model, using=self._db)    


class ResourceModel(gis_models.Model):

    objects = ResourceManager.from_queryset(ResourceQuerySet)()
    unique_key = "location"


    class Meta:
        abstract = True

    @classmethod
    def get_location(cls, data:Any) -> Point:
        msg = f"{cls.__name__} must implement the `get_location` method."
        logger.error(msg, exc_info=True)
        raise NotImplementedError(msg)

    @staticmethod
    def get_point(lon:float, lat:float) -> Point:
        return Point(x=lon, y=lat, srid=4326)

    @classmethod
    def normalize_data(cls, data:dict[str, Any]):
        msg = f"{cls.__name__} must implement the `normalize_data` method."
        logger.error(msg, exc_info=True)
        raise NotImplementedError(msg)  

    @classmethod
    def validate_unique_key(cls):
        """
        Ensures the model defines a valid `unique_key` attribute.

        This method is typically used before dynamically constructing 
        database filter queries to ensure that any errors occur at the 
        application level, rather than causing database-level errors.
        """
        if not hasattr(cls, cls.unique_key):
            raise AttributeError(f"Model {cls.__name__} must define a valid unique_key.")


    # def save(self, **kwargs):
    #     super().save(**kwargs)