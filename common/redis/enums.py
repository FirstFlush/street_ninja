from common.base_enum import StreetNinjaEnum


class RedisStoreEnum(StreetNinjaEnum):
    DEFAULT = "default"
    SESSION = "session"
    PHONE_SESSION = "phone_session"
    RESOURCES = "resources"
    CELERY = "celery"


class RedisKeyEnum(StreetNinjaEnum):
    ...


class ResourceKeyEnum(RedisKeyEnum):
    """Redis key for querysets cached in redis resources cache."""
    SHELTER = "shelter:all"
    FOOD = "food:all"
    WATER = "water:all"
    TOILET = "toilet:all"
    WIFI = "wifi:all"


class PhoneSessionFieldsEnum(StreetNinjaEnum):

    KEYWORD = "keyword"
    ORDER = "order"
    OFFSET = "offset"
    LAST_UPDATED = "last_updated"


class RedisKeyTTL(StreetNinjaEnum):
    """TTL for resource data in redis cache in seconds"""
    # TWENTY_SECONDS = 20 # for testing
    MINUTE = 60   
    MINUTES_FIFTEEN = 900 
    MINUTES_THIRTY = 1800           
    HOUR = 3600                 
    HOURS_FOUR = 14400            
