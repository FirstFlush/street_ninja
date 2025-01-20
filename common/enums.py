from .base_enum import StreetNinjaEnum


class SMSKeyword(StreetNinjaEnum):
    """
    Enum representing the SMS keywords users can text to the Street Ninja app 
    to locate specific resources.

    Keywords:
        - FOOD: Information about nearest meal services or food resources.
        - SHELTER: Assistance finding nearest available shelters.
        - WATER: Locations for accessing nearest clean drinking water.
        - TOILET: Public or accessible restrooms nearby.
        - WIFI: Closest available public WiFi.

    These keywords are case-insensitive when used by the app's SMS interface.
    """
    FOOD = "FOOD"
    SHELTER = "SHELTER"
    WATER = "WATER"
    TOILET = "TOILET"
    WIFI = "WIFI"


class RedisStoreEnum(StreetNinjaEnum):
    DEFAULT = 0
    SESSION = 1
    INQUIRY = 2
    GEODATA = 3
    CELERY = 4
    

class InquiryStatus(StreetNinjaEnum):
    """Status of a SMS message inquiry"""
    PENDING = 'pending'
    PROCESSED = 'processed'
    ERROR = 'error'


class GeocoderEnum(StreetNinjaEnum):
    NOMINATIM = "Nominatim"
    OPENCAGE = "OpenCage"
    # POSITIONSTACK = "positionstack"


class HttpMethodEnum(StreetNinjaEnum):
    """
    Enum representing HTTP methods.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"