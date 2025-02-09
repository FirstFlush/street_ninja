from .base_enum import StreetNinjaEnum



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
