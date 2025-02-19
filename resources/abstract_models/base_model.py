import logging
from typing import Any
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class ResourceQuerySet(gis_models.QuerySet):
    """
    Custom queryset for Resource model with geospatial filtering.
    """

    def closest_to(self, location:Point) -> "ResourceQuerySet":
        """
        Returns a queryset of resources ordered by distance from the given location.

        NOTE not in use because annotate() method causes a DB hit. 
        Substituted instead for the geo.geospatial_service.GeospatialService.sort_by_distance() method
        """
        return self.annotate(
            distance=Distance("location", location)).order_by("distance")


class ResourceManager(gis_models.Manager):

    def get_queryset(self):
        return ResourceQuerySet(self.model, using=self._db)    


class ResourceModel(gis_models.Model):

    objects = ResourceManager.from_queryset(ResourceQuerySet)()
    _unique_key = "location"
    _keyword_enum = None

    class Meta:
        abstract = True

    @property
    def keyword_enum(self) -> SMSKeywordEnum:
        try:
            return SMSKeywordEnum(self._keyword_enum)
        except ValueError as e:
            msg = f"Invalid _keyword_enum `{self._keyword_enum}` for resource model `{self.__class__.__name__}`"
            logger.error(msg, exc_info=True)
            raise

    @property
    def map_values(self) -> dict[str, Any]:
        """
        This property must be implemented in child classes.
        Prepares data for the Street Ninja website's interactive map.
        """
        msg = f"{self.__class__.__name__} must implement map_values()"
        logger.error(msg)
        raise NotImplementedError(msg)

    @classmethod
    def get_location(cls, data:Any) -> Point:
        msg = f"{cls.__name__} must implement the `get_location` method."
        logger.error(msg)
        raise NotImplementedError(msg)

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
        if not hasattr(cls, cls._unique_key):
            raise AttributeError(f"Model {cls.__name__} must define a valid _unique_key.")

    @staticmethod
    def get_point(lon:float, lat:float) -> Point:
        return Point(x=lon, y=lat, srid=4326)