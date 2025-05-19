from dataclasses import dataclass
from django.contrib.gis.geos import Point


@dataclass
class NeighborhoodCacheData:
    name: str
    name_normalized: str
    centroid: Point 