import logging
from geopy.distance import distance
from django.contrib.gis.geos import Point
from .exc import GeospatialException
from resources.abstract_models import ResourceModel


logger = logging.getLogger(__name__)


class GeospatialService:
    """Handles geospatial calculations for cached resources."""

    def __init__(self, resources: list[ResourceModel], location: Point):
        self.resources = resources
        self.location = location
        if not isinstance(resources, list):
            msg = f"Expected a list of ResourceModel objects, got type `{type(resources)}`"
            logger.error(msg)
            raise TypeError(msg)
        if not all(hasattr(obj, "location") and isinstance(obj.location, Point) for obj in resources):
            msg = "All resource objects must have a valid location attribute of type Point"
            logger.error(msg)
            raise AttributeError(msg)


    def _sort(self) -> list[ResourceModel]:
        """Sorts resources by distance and adds a `.distance` attribute to each."""
        for obj in self.resources:
            obj.distance = round(distance((self.location.y, self.location.x), (obj.location.y, obj.location.x)).km, 1) 
        return sorted(self.resources, key=lambda obj: obj.distance)


    @classmethod
    def sort_by_distance(cls, resources: list[ResourceModel], location: Point) -> list[ResourceModel]:
        """Creates a GeoSpatialService instance and sorts resources by distance."""
        try:
            geospatial_service = cls(resources=resources, location=location)
            return geospatial_service._sort()
        except Exception as e:
            msg = f"GeospatialService failed due to unexpected `{e.__class__.__name__}`: {e}"
            logger.error(msg, exc_info=True)
            raise GeospatialException(msg) from e