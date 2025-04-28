"""
Common utility functions
"""
import logging
from datetime import datetime, timezone
from django.contrib.gis.geos import Point


logger = logging.getLogger(__name__)


def convert_bool(value: bool, abbreviated: bool = True) -> str:
    if isinstance(value, bool):
        if abbreviated:
            return "Y" if value else "N"
        else:
            return "Yes" if value else "No"
    msg = f"`{cls.__name__}`.convert_bool() Received invalid type for param value: `{type(value)}`, value `{value}`"
    logger.error(msg)
    raise TypeError(msg)


def now() -> datetime:
    return datetime.now(tz=timezone.utc)

def get_point(x:float, y:float) -> Point:
    return Point(x=x, y=y)

def coord_string(point: Point) -> str:
    """
    This is required for OpenRouteService as their API requires coordinates in this format.
    This might be useful for other APIs in the future so that's why it's in utils.
    """
    return f"{point.x},{point.y}"