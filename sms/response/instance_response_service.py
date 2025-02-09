from .base_response_service import BaseResponseService
from .respones_templates.base_response_templates import FollowUpResponseTemplate
from sms.enums import SMSFollowUpKeywordEnum



class InstanceResponseService(BaseResponseService):
    
    MAPPING: dict[SMSFollowUpKeywordEnum, FollowUpResponseTemplate] = {

    }