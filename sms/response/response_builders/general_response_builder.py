from .base_response_builder import BaseResponseBuilder
from ..response_templates.base_response_templates import BaseSMSResponseTemplate
from sms.enums import SMSFollowUpKeywordEnum



class GeneralResponseBuilder(BaseResponseBuilder):
    ...
    # MAPPING: dict[SMSFollowUpKeywordEnum, BaseSMSResponseTemplate] = {
    #     # SMSFollowUpKeywordEnum.DIRECTIONS: 
    # }