from .base_access_patterns import BaseRedisAccessPattern
from ..enums import RedisStoreEnum, RedisKeyTTL, PhoneSessionFieldsEnum


class PhoneSessionAccessPattern(BaseRedisAccessPattern):
    
    redis_key_format = "phone_session:{phone_number}"
    session_fields = PhoneSessionFieldsEnum.values


# class ConversationAccessPattern(AccessPatternKV):

#     redis_store_enum = RedisStoreEnum.PHONE_SESSION
#     redis_key_enum = PhoneSessionKeyEnum

# class KeywordAccessPattern(AccessPatternKV):

#     redis_store_enum = RedisStoreEnum.PHONE_SESSION
#     redis_key_enum = PhoneSessionKeyEnum.KEYWORD
#     # key_ttl_enum = 
#     something = "phone_session:{phone_number}"
#     value = None