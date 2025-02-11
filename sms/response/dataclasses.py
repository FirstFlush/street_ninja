from dataclasses import dataclass
from typing import Optional
from sms.models import SMSInquiry
from cache.dataclasses import PhoneSessionData
from cache.follow_up_caching_service import FollowUpCachingService


@dataclass
class FollowUpContext:
    sms_inquiry: SMSInquiry
    current_session: PhoneSessionData
    caching_service: FollowUpCachingService


@dataclass
class BaseResponseData:
    msg: str

@dataclass
class SMSInquiryResponseData(BaseResponseData):
    ids: list[int]

    @property
    def offset(self) -> int:
        return len(self.ids)

@dataclass
class SMSFollowUpResponseData(BaseResponseData):
    ids: Optional[list[int]] = None
    directions_text: Optional[str] = None 
    # params: Optional[dict[str, Any]] = None