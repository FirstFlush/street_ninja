import logging
from sms.enums import SMSKeywordEnum
from .base_access_patterns import AccessPatternDB
from .resources import (
    ShelterAccessPattern,
    FoodProgramAccessPattern,
    ToiletAccessPattern,
    DrinkingFountainAccessPattern,
    PublicWifiAccessPattern,
)


logger = logging.getLogger(__name__)


class AccessPatternRegistry:
    _resource_patterns = {
        SMSKeywordEnum.FOOD: FoodProgramAccessPattern,
        SMSKeywordEnum.SHELTER: ShelterAccessPattern,
        SMSKeywordEnum.WATER: DrinkingFountainAccessPattern,
        SMSKeywordEnum.TOILET: ToiletAccessPattern,
        SMSKeywordEnum.WIFI: PublicWifiAccessPattern,
    }

    @classmethod
    def get_pattern(cls, sms_keyword_enum: SMSKeywordEnum)-> AccessPatternDB:
        """Retrieves the correct access pattern for the given resource type."""
        try:
            return cls._resource_patterns[sms_keyword_enum]
        except KeyError:
            msg = f"Can not find cache AccessPattern for sms_keyword_enum: {sms_keyword_enum}"
            logger.error(msg, exc_info=True)
            raise
