from dataclasses import dataclass
from typing import Optional, Type
from resources.abstract_models import ResourceQuerySet, ResourceModel
from sms.models import SMSInquiry, SMSFollowUpInquiry
from sms.response.response_templates import QuerySetResponseTemplate, GeneralResponseTemplate
from cache.dataclasses import PhoneSessionData
from cache.follow_up_caching_service import FollowUpCachingService
from cache.inquiry_caching_service import InquiryCachingService


@dataclass
class InquiryResponseContext:
    instance: SMSInquiry
    caching_service: InquiryCachingService
    queryset: ResourceQuerySet


@dataclass
class FollowUpContext:
    sms_inquiry: SMSInquiry
    follow_up_inquiry: SMSFollowUpInquiry
    current_session: PhoneSessionData
    caching_service: FollowUpCachingService


@dataclass
class BaseResponseData:
    template: QuerySetResponseTemplate | GeneralResponseTemplate
    msg: str
    ids: list[int]


@dataclass
class SMSInquiryResponseData(BaseResponseData):

    template: QuerySetResponseTemplate

    @property
    def offset(self) -> int:
        return len(self.ids)


@dataclass
class SMSFollowUpResponseData(BaseResponseData):

    ids: Optional[list[int]] = None             # MORE needs ids
    resource: Optional[ResourceModel] = None    # INFO & DIRECTIONS need resource
    # directions: Optional[list[str]] = None       # DIRECTIONS needs directions_text
