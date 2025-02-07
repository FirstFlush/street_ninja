from .base_enum import StreetNinjaEnum


class SMSKeywordEnum(StreetNinjaEnum):
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
    HELP = "HELP"
    # MORE = "MORE"


class LocationType(StreetNinjaEnum):
    ADDRESS = "address"
    INTERSECTION = "intersection"
    LANDMARK = "landmark"


class LanguageEnum(StreetNinjaEnum):
    ENGLISH = "en"
    FRENCH = "fr"
    PUNJABI = "pa"
    CHINESE = "zh" # includes both Mandarin and Cantonese
    YORUBA = "yo"


class InquiryStatusEnum(StreetNinjaEnum):
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

class TTLSecondsEnum(StreetNinjaEnum):
    MINUTE = 60   
    MINUTES_FIFTEEN = 900 
    MINUTES_THIRTY = 1800           
    HOUR = 3600                 
    HOURS_FOUR = 14400            
