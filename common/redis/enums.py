from common.base_enum import StreetNinjaEnum


class RedisStoreEnum(StreetNinjaEnum):
    DEFAULT = "default"
    SESSION = "session"
    PHONE_SESSIONR = "phone_session"
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


class RedisKeyTTL(StreetNinjaEnum):
    """TTL for resource data in redis cache"""
    SHELTER = 60                # 1 minute
    FOOD = 3600                 # 1 hours
    TOILET = 14400              # 4 hours
    WATER = 14400               # 4 hours
    WIFI = 3600                 # 1 hour
    PHONE_SESSION_RESULTS = 900 # 15 minutes