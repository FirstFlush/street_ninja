from .base_response_builder import BaseResponseBuilder
from .respones_templates.base_response_templates import FollowUpResponseTemplate
from sms.enums import SMSFollowUpKeywordEnum



class InstanceResponseBuilder(BaseResponseBuilder):
    
    MAPPING: dict[SMSFollowUpKeywordEnum, FollowUpResponseTemplate] = {
        # SMSFollowUpKeywordEnum.DIRECTIONS: 
    }