import logging
from cache.dataclasses import PhoneSessionData
from cache.redis.exc import NoSessionFound
from cache.follow_up_caching_service import FollowUpCachingService
from cache.inquiry_caching_service import InquiryCachingService
from common.utils import coord_string
from sms.enums import SMSFollowUpKeywordEnum
from .follow_up import More, DirectionsHandler, InfoHandler
from sms.models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry
from .dataclasses import SMSInquiryResponseData, SMSFollowUpResponseData, FollowUpContext, InquiryResponseContext
from .inquiry_response_handler import InquiryResponseHandler
from .response_templates.help_template import HelpResponseTemplate
from .exc import SendHelpError

logger = logging.getLogger(__name__)


class ResponseService:

    def __init__(self, instance: SMSInquiry | SMSFollowUpInquiry | UnresolvedSMSInquiry):
        self.instance = instance

    def build_response_data(self) -> SMSInquiryResponseData | SMSFollowUpResponseData | None:
        """
        Processes the inquiry and generates a response according to its type.

        Each type will produce a datatype with the information required for
        the persistence layer to create the SMS Response object, and the
        caching layer to update and necessary ephemeral data.
        """
        try:
            if isinstance(self.instance, SMSInquiry):
                response_data = self._build_inquiry_response_data()
            elif isinstance(self.instance, SMSFollowUpInquiry):
                response_data = self._build_follow_up_response_data()
            elif isinstance(self.instance, UnresolvedSMSInquiry):
                response_data = None
            else:
                msg = f"Received invalid type for instance argument: `{type(self.instance)}`"
                logger.error(msg)
                raise TypeError(msg)
        except SendHelpError:
            response_data = None

        return response_data

    def _build_inquiry_response_data(self) -> SMSInquiryResponseData:
        
        caching_service = InquiryCachingService.init(inquiry=self.instance)
        resources = caching_service.get_resources_by_proximity(
            location=self.instance.location, 
            inquiry_params=self.instance.params
        )
        context = InquiryResponseContext(
            instance=self.instance,
            caching_service=caching_service,
            resources=resources,
        )
        inquiry_response_handler = InquiryResponseHandler(context=context)
        response_data = inquiry_response_handler.build_response_data()
        return response_data

    def _get_sms_inquiry_for_follow_up(self, id: int) -> SMSInquiry:
        """
        When a follow-up request comes in, it needs to be matched to an SMS inquiry.
        """
        sms_inquiry = self.instance.conversation.smsinquiry_set.filter(id=id).first()
        if not sms_inquiry:
            msg = f"No SMSInquiry found in session cache with ID of `{id}` when processing SMSFollowUpInquiry with ID of `{self.instance.id}`"
            logger.error(msg)
            raise ValueError(msg)
        return sms_inquiry

    def _build_follow_up_context(
            self,
            sms_inquiry: SMSInquiry,
            current_session: PhoneSessionData,
            caching_service: FollowUpCachingService,
    ) -> FollowUpContext:
        return FollowUpContext(
            sms_inquiry=sms_inquiry,
            current_session=current_session,
            caching_service=caching_service,
            follow_up_inquiry=self.instance,
        )

    def _build_follow_up_response_data(self) -> SMSFollowUpResponseData | None:

        try:
            caching_service, current_session = FollowUpCachingService.init(follow_up_inquiry=self.instance)
        except NoSessionFound as e:
            logger.warning(e)
            return None
            
        sms_inquiry = self._get_sms_inquiry_for_follow_up(current_session.inquiry_id)
        context = self._build_follow_up_context(
            sms_inquiry=sms_inquiry,
            current_session=current_session,
            caching_service=caching_service,
        )
        match self.instance.keyword_enum:
            case SMSFollowUpKeywordEnum.DIRECTIONS:
                start_coords = coord_string(sms_inquiry.location)
                directions_handler = DirectionsHandler(context=context)
                directions_handler.set_directions(start_coords=start_coords)
                response_data = directions_handler.build_response_data()
                directions_handler.update_session()
            case SMSFollowUpKeywordEnum.INFO:
                info_handler = InfoHandler(context=context)
                response_data = info_handler.build_response_data()
                info_handler.update_session()
            case SMSFollowUpKeywordEnum.MORE:
                more_handler = More(context=context)
                response_data = more_handler.build_response_data()
                more_handler.update_session(ids=response_data.ids)
        return response_data


    def build_help_msg(self) -> str:
        return HelpResponseTemplate.help_msg()