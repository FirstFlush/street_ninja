import logging
from cache.follow_up_caching_service import FollowUpCachingService
from cache.inquiry_caching_service import InquiryCachingService
from sms.enums import SMSKeywordEnum, SMSFollowUpKeywordEnum
from sms.models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry
from .dataclasses import SMSInquiryResponseData, SMSFollowUpResponseData
from .queryset_response_builder import QuerySetResponseBuilder
from .instance_response_builder import InstanceResponseBuilder


logger = logging.getLogger(__name__)


class ResponseService:

    def __init__(self, instance: SMSInquiry | SMSFollowUpInquiry | UnresolvedSMSInquiry):
        self.instance = instance


    def build_response_data(self) -> SMSInquiryResponseData | SMSFollowUpResponseData:
        """
        Processes the inquiry and generates a response according to its type.

        Each type will produce a datatype with the information required for
        the persistence layer to create the SMS Response object, and the
        caching layer to update and necessary ephemeral data.
        """
        if isinstance(self.instance, SMSInquiry):
            response = self._build_inquiry_response_data(self.instance)
        elif isinstance(self.instance, SMSFollowUpInquiry):
            response = self._build_follow_up_response(self.instance)
        elif isinstance(self.instance, UnresolvedSMSInquiry):
            response = self._build_unresolved_response(self.instance)
        else:
            msg = f"Received invalid type for instance argument: `{type(self.instance)}`"
            logger.error(msg)
            raise TypeError(msg)
        return response 
    
    
    def _build_inquiry_response_data(self, instance: SMSInquiry) -> SMSInquiryResponseData:
        
        caching_service = InquiryCachingService.init(inquiry=instance)
        session_data = caching_service.get_phone_session()
        offset = session_data.offset if session_data is not None else 0
        qs = caching_service.get_resources_by_proximity(location=instance.location)
        response_service = QuerySetResponseBuilder(
            queryset=qs,
            offset=offset,
        )
        response_data = response_service.create_response_data()
        if session_data:
            session_data = caching_service.update_phone_session(
                session_data=session_data,
                ids=response_data.ids,
            )
        else:
            session_data =caching_service.create_phone_session(
                ids=response_data.ids,
                params=instance.params if instance.params else None,
            )
        return response_data


    def _build_follow_up_response(self, instance: SMSFollowUpInquiry):

        caching_service, current_session = FollowUpCachingService.init(follow_up_inquiry=instance)
        match instance.keyword_enum:
            case SMSFollowUpKeywordEnum.DIRECTIONS:
                ...
            case SMSFollowUpKeywordEnum.INFO:
                ...
            case SMSFollowUpKeywordEnum.MORE:
                caching_service.more()

    def _build_unresolved_response(self, instance: UnresolvedSMSInquiry):
        ...