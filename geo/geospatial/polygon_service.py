from django.contrib.gis.geos import Point, Polygon
from shapely import Polygon as ShapelyPolygon


class PolygonService:

    @staticmethod
    def create_polygon_from_list_of_points(points: list[Point]) -> Polygon:
        return Polygon([(pt.x, pt.y) for pt in points])

    @staticmethod
    def get_centroid(boundary_coordinates: list[tuple[int, int]]) -> Point:
        polygon = ShapelyPolygon(boundary_coordinates)
        return Point(x=polygon.centroid.x, y=polygon.centroid.y)
