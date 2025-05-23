import random
from typing import Type
from cache.redis.access_patterns.base_access_patterns import AccessPatternDB 
from street_ninja_server.global_mappings import ACCESS_PATTERN_TO_MODEL


def generate_id_list() -> list[int]:
    return [random.randint(1, 200) for _ in range (random.randint(3, 15))]


def all_access_patterns() -> list[Type[AccessPatternDB]]:
    return list(ACCESS_PATTERN_TO_MODEL.keys())