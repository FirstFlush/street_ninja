from dataclasses import dataclass
from django.contrib.gis.geos import Point


@dataclass
class IncomingNeighborhoodData:
    name: str
    coordinates: list[Point]
    centroid: Point


@dataclass
class NeighborhoodCacheData:
    name: str
    name_normalized: str
    centroid: Point 
    
