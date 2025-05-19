from common.base_enum import StreetNinjaEnum


class RedisStoreEnum(StreetNinjaEnum):
    DEFAULT = "default"
    SESSION = "session"
    PHONE_SESSION = "phone_session"
    RESOURCES = "resources"
    CELERY = "celery"
    GEO = "geo"
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


class GeoKeyEnum(RedisKeyEnum):
    LOCATION_MAPPING = "location_mapping:all"
    NEIGHBORHOODS = "neighborhoods:all"


class TestKeyEnum(RedisKeyEnum):
    LOCATION_MAPPING = "tests:location_mapping:all"
    SHELTER = "tests:shelter:all"
    FOOD = "tests:food:all"
    WATER = "tests:water:all"
    TOILET = "tests:toilet:all"
    WIFI = "tests:wifi:all"
    PHONE_SESSION = "tests:phone_session"
    NEIGHBORHOODS = "tests:neighborhoods:all"




class RedisKeyTTL(StreetNinjaEnum):
    """TTL for resource data in redis cache in seconds"""
    # TWENTY_SECONDS = 20  # for testing purposes
    MINUTE = 60   
    MINUTES_FIFTEEN = 900 
    MINUTES_THIRTY = 1800           
    HOUR = 3600                 
    HOURS_FOUR = 14400
    DAY = 86400
