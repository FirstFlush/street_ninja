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
    model_cls = Shelter
    query = Shelter.objects.filter


class FoodProgramAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.FOOD
    key_ttl_enum = RedisKeyTTL.HOUR
    model_cls = FoodProgram
    query = FoodProgram.objects.filter


class DrinkingFountainAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.WATER
    key_ttl_enum = RedisKeyTTL.HOURS_FOUR
    model_cls = DrinkingFountain
    query = DrinkingFountain.objects.filter


class ToiletAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.TOILET
    key_ttl_enum = RedisKeyTTL.HOURS_FOUR
    model_cls = Toilet
    query = Toilet.objects.filter


class PublicWifiAccessPattern(AccessPatternDB):

    redis_store_enum = RedisStoreEnum.RESOURCES
    redis_key_enum = ResourceKeyEnum.WIFI
    key_ttl_enum = RedisKeyTTL.HOUR
    model_cls = PublicWifi
    query = PublicWifi.objects.filter