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

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.WATER
    key_ttl_enum = RedisKeyTTL.HOURS_FOUR
    query = DrinkingFountain.objects.filter


class ToiletAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.TOILET
    key_ttl_enum = RedisKeyTTL.HOURS_FOUR
    query = Toilet.objects.filter


class PublicWifiAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.WIFI
    key_ttl_enum = RedisKeyTTL.HOUR
    query = PublicWifi.objects.filter