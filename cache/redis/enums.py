from common.base_enum import StreetNinjaEnum


class RedisStoreEnum(StreetNinjaEnum):
    DEFAULT = "default"
    SESSION = "session"
    PHONE_SESSION = "phone_session"
    RESOURCES = "resources"
    CELERY = "celery"
    LOCATION = "location"
    TESTS = "tests"


class RedisKeyEnum(StreetNinjaEnum):
    ...


class ResourceKeyEnum(RedisKeyEnum):
    """Redis key for querysets cached in redis resources cache."""
    SHELTER = "shelter:all"
    FOOD = "food:all"
    WATER = "water:all"
    TOILET = "toilet:all"
    WIFI = "wifi:all"


class WebSessionKeyEnum(RedisKeyEnum):
    PHONE = "phone"


class LocationKeyEnum(RedisKeyEnum):
    MAPPING = "location_mapping:all"


class TestKeyEnum(RedisKeyEnum):
    MAPPING = "tests:location_mapping:all"




class RedisKeyTTL(StreetNinjaEnum):
    """TTL for resource data in redis cache in seconds"""
    # TWENTY_SECONDS = 20  # for testing purposes
    MINUTE = 60   
    MINUTES_FIFTEEN = 900 
    MINUTES_THIRTY = 1800           
    HOUR = 3600                 
    HOURS_FOUR = 14400
    DAY = 86400
