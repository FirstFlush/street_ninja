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
            response = self._build_inquiry_response_data()
        elif isinstance(self.instance, SMSFollowUpInquiry):
            response = self._build_follow_up_response()
        elif isinstance(self.instance, UnresolvedSMSInquiry):
            response = self._build_unresolved_response()
        else:
            msg = f"Received invalid type for instance argument: `{type(self.instance)}`"
            logger.error(msg)
            raise TypeError(msg)
        return response 


    def _build_inquiry_response_data(self) -> SMSInquiryResponseData:
        
        caching_service = InquiryCachingService.init(inquiry=self.instance)
        session_data = caching_service.get_phone_session()
        # offset = session_data.offset if session_data is not None else 0
        offset = 0
        qs = caching_service.get_resources_by_proximity(location=self.instance.location)
        response_builder = QuerySetResponseBuilder(
            queryset=qs,
            offset=offset,
        )
        response_data = response_builder.create_response_data()
        if session_data:
            session_data = caching_service.update_phone_session(
                session_data=session_data,
                ids=response_data.ids,
            )
        else:
            session_data =caching_service.create_phone_session(
                ids=response_data.ids,
                params=self.instance.params if self.instance.params else None,
            )
        return response_data

    def _get_sms_inquiry_for_follow_up(self, id: int) -> SMSInquiry:
        sms_inquiry = self.instance.conversation.smsinquiry_set.filter(id=id).first()
        if not sms_inquiry:
            msg = f"No SMSInquiry found in session cache with ID of `{id}` when processing SMSFollowUpInquiry with ID of `{self.instance.id}`"
            logger.error(msg)
            raise ValueError(msg)
        return sms_inquiry


    def _build_follow_up_response(self):
        caching_service, current_session = FollowUpCachingService.init(follow_up_inquiry=self.instance)
        sms_inquiry = self._get_sms_inquiry_for_follow_up(current_session.inquiry_id)
        match self.instance.keyword_enum:
            case SMSFollowUpKeywordEnum.DIRECTIONS:
                ...
            case SMSFollowUpKeywordEnum.INFO:
                ...
            case SMSFollowUpKeywordEnum.MORE:
                qs = caching_service.get_resources_by_proximity(location=sms_inquiry.location)
                response_service = QuerySetResponseBuilder(
                    queryset=qs,
                    offset=current_session.offset,
                )
                response_data = response_service.create_response_data()
                print()
                print(current_session)
                print()
                print(response_data)
                print()
                # TODO: update session!
                # caching_service.more(current_session)

    def _build_unresolved_response(self):
        ...
