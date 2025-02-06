from abc import ABC
from dataclasses import dataclass
from typing import Callable, Optional
from ..enums import RedisKeyEnum, RedisStoreEnum, RedisKeyTTL


@dataclass
class BaseRedisAccessPattern(ABC):
    redis_store_enum: RedisStoreEnum
    key_ttl_enum: RedisKeyTTL


@dataclass
class AccessPatternDB(BaseRedisAccessPattern):
    redis_key_enum: RedisKeyEnum
    query: Optional[Callable] = None


# @dataclass
# class AccessPatternKV(BaseRedisAccessPattern):
#     value: Optional[Any] = None