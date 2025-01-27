from .base_access_patterns import AccessPatternDB, AccessPatternKV
from .enums import RedisStoreEnum, RedisKeyTTL, ResourceKeyEnum
from resources.models import (
    Shelter,
    FoodProgram,
)

class ShelterAccessPattern(AccessPatternDB):

    redis_key_enum = ResourceKeyEnum.SHELTER
    redis_store_enum = RedisStoreEnum.RESOURCES
    key_ttl_enum = RedisKeyTTL.SHELTER
    query = Shelter.objects.all


class FoodProgramAccessPattern(AccessPatternDB):

    redis_key_enum = ResourceKeyEnum.FOOD
    redis_store_enum = RedisStoreEnum.RESOURCES
    key_ttl_enum = RedisKeyTTL.FOOD
    query = FoodProgram.objects.all