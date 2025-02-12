from dataclasses import dataclass
from typing import Optional, Type
from resources.abstract_models import ResourceQuerySet
from sms.models import SMSInquiry
from sms.response.response_templates import QuerySetResponseTemplate
from cache.dataclasses import PhoneSessionData
from cache.follow_up_caching_service import FollowUpCachingService
from cache.inquiry_caching_service import InquiryCachingService


@dataclass
class InquiryResponseContext:
    instance: SMSInquiry
    caching_service: InquiryCachingService
    queryset: ResourceQuerySet


# @dataclass
# class MetaContext:
#     top: str
#     bottom: str


@dataclass
class FollowUpContext:
    sms_inquiry: SMSInquiry
    current_session: PhoneSessionData
    caching_service: FollowUpCachingService


@dataclass
class BaseResponseData:
    msg: str
    ids: list[int]


@dataclass
class SMSInquiryResponseData(BaseResponseData):

    template_class: Type[QuerySetResponseTemplate]

    @property
    def offset(self) -> int:
        return len(self.ids)


@dataclass
class SMSFollowUpResponseData(BaseResponseData):
    ids: Optional[list[int]] = None
    directions_text: Optional[str] = None 
    # params: Optional[dict[str, Any]] = None