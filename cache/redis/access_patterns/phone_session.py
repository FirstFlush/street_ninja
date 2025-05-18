from django.conf import settings
from .base_access_patterns import BaseRedisAccessPattern
from ..enums import RedisStoreEnum, RedisKeyTTL


class PhoneSessionAccessPattern(BaseRedisAccessPattern):
    
    redis_store_enum = RedisStoreEnum.PHONE_SESSION
    redis_key_format = "phone_session:"  # phone_session:<conversation_id>
    key_ttl_enum = RedisKeyTTL(settings.TTL_PHONE_SESSION)
