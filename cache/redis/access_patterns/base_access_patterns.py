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

from abc import ABC
from dataclasses import dataclass
from django.db.models import Model
from typing import Callable, Optional, Type
from ..enums import RedisKeyEnum, RedisStoreEnum, RedisKeyTTL


@dataclass
class BaseRedisAccessPattern(ABC):
    redis_store_enum: RedisStoreEnum
    key_ttl_enum: RedisKeyTTL


@dataclass
class AccessPatternDB(BaseRedisAccessPattern):
    redis_key_enum: RedisKeyEnum
    expected_type: Type[object]
    query: Optional[Callable] = None


# @dataclass
# class AccessPatternKV(BaseRedisAccessPattern):
#     value: Optional[Any] = None