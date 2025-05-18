from dataclasses import dataclass
from django.contrib.gis.geos import Point


@dataclass
class NeighborhoodData:
    name: str
    coordinates: list[Point]
    centroid: Point