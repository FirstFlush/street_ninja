import logging
from sms.enums import SMSKeywordEnum
from street_ninja_server.global_mappings import SMS_KEYWORD_ENUM_TO_ACCESS_PATTERN
from .base_access_patterns import AccessPatternDB


logger = logging.getLogger(__name__)


class AccessPatternRegistry:
    _resource_patterns = SMS_KEYWORD_ENUM_TO_ACCESS_PATTERN

    @classmethod
    def get_pattern(cls, sms_keyword_enum: SMSKeywordEnum)-> AccessPatternDB:
        """Retrieves the correct access pattern for the given resource type."""
        try:
            return cls._resource_patterns[sms_keyword_enum]
        except KeyError:
            msg = f"Can not find cache AccessPattern for sms_keyword_enum: {sms_keyword_enum}"
            logger.error(msg, exc_info=True)
            raise
