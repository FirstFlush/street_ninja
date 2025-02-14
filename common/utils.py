"""
Common utility functions
"""
from datetime import datetime, timezone
from django.contrib.gis.geos import Point


def now() -> datetime:
    return datetime.now(tz=timezone.utc)


def coord_string(point: Point) -> str:
    """
    This is required for OpenRouteService as their API requires coordinates in this format.
    This might be useful for other APIs in the future so that's why it's in utils.
    """
    return f"{point.x},{point.y}"