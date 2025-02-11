from abc import ABC, abstractmethod
from cache.follow_up_caching_service import FollowUpCachingService
from cache.dataclasses import PhoneSessionData
from sms.models import SMSInquiry
from sms.response.dataclasses import FollowUpContext, SMSFollowUpResponseData


class BaseFollowUpHandler(ABC):

    @abstractmethod
    def build_response_data(self, context: FollowUpContext) -> SMSFollowUpResponseData:
        ...