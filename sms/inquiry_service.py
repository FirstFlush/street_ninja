import logging
from .models import SMSInquiry
from common.redis.access_patterns import (
    AccessPatternDB,
    ShelterAccessPattern,
    FoodProgramAccessPattern,
    ToiletAccessPattern,
    DrinkingFountainAccessPattern,
    PublicWifiAccessPattern,
)
from common.redis.access_patterns import AccessPatternRegistry


logger = logging.getLogger(__name__)


class InquiryProcessingService:

    def __init__(self, inquiry: SMSInquiry, access_pattern: AccessPatternDB):
        self.inquiry = inquiry
        self.access_pattern = access_pattern

    @classmethod
    def init(cls, inquiry: SMSInquiry) -> "InquiryProcessingService":
        """
        Factory method for selecting instantiating InquiryProcessingService 
        with the inquiry's appropriate access pattern.
        """
        access_pattern = AccessPatternRegistry.get_resource(sms_keyword_enum=inquiry.keyword_enum)
        logger.info(f"Access pattern `{access_pattern.__class__.__name__}` loaded for SMSInquiry ID `{inquiry.id}`")
        return cls(
            inquiry=inquiry, 
            access_pattern=access_pattern,
        )
    
