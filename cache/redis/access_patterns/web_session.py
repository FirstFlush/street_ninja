from .base_access_patterns import BaseRedisAccessPattern
from ..enums import RedisStoreEnum, RedisKeyTTL, WebSessionKeyEnum


class WebSessionAccessPattern(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.SESSION
    redis_key_enum = WebSessionKeyEnum.PHONE
    key_ttl_enum = RedisKeyTTL.MINUTES_THIRTY