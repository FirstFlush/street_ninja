"""
Redis Access Patterns

This file defines **all** Redis Access Patterns for the application. 
An access pattern is a standardized, pre-defined configuration that 
describes how the application interacts with Redis for a specific use case.

Access patterns are essentially keys to the redis store that define:
    - Which key to use in Redis (`redis_key_enum`)
    - Which Redis store to use (`redis_store_enum`)
    - The time-to-live for the key (`key_ttl_enum`)
    - The data source (`query` or `value`):
        - For DB-backed access patterns, this defines the query logic used to 
        fetch data when a cache miss occurs.
        - For key-value access patterns, this defines the value to be stored 
        in Redis if the stored value is None/missing.

By enforcing access patterns, this file ensures all Redis interactions 
are centralized, consistent, and maintainable. 

You **cannot** interact with the Redis client directly; instead, you must 
define or use an existing access pattern.

*See ./registry.py for a registry mapping enums to access patterns.
"""
from .base_access_patterns import AccessPatternDB
from ..enums import RedisStoreEnum, RedisKeyTTL, ResourceKeyEnum
from resources.models import (
    Shelter,
    FoodProgram,
    DrinkingFountain,
    Toilet,
    PublicWifi,
)


class ShelterAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.SHELTER
    key_ttl_enum = RedisKeyTTL.HOUR
    query = Shelter.objects.filter


class FoodProgramAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.FOOD
    key_ttl_enum = RedisKeyTTL.HOUR
    query = FoodProgram.objects.filter


class DrinkingFountainAccessPattern(AccessPatternDB):

    redis_key_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.WATER
    key_ttl_enum = RedisKeyTTL.HOURS_FOUR
    query = DrinkingFountain.objects.filter


class ToiletAccessPattern(AccessPatternDB):

    redis_key_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.TOILET
    key_ttl_enum = RedisKeyTTL.HOURS_FOUR
    query = Toilet.objects.filter


class PublicWifiAccessPattern(AccessPatternDB):

    redis_key_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.WIFI
    key_ttl_enum = RedisKeyTTL.HOUR
    query = PublicWifi.objects.filter