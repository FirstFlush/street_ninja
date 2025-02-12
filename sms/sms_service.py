import logging
from django.contrib.gis.geos import Point
from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS, 
)
# from sms.response.respones_templates import ResourceResponseTemplate
from sms.response import (
    SMSInquiryResponseData, 
    SMSFollowUpResponseData,
    ResponseService,
)
from sms.persistence_service import PersistenceService
from sms.enums import ResolvedSMSType, SMSKeywordEnum, SMSFollowUpKeywordEnum
from geo.geocoding import GeocodingService
from .abstract_models import IncomingSMSMessageModel
from cache.follow_up_caching_service import FollowUpCachingService
from cache.inquiry_caching_service import InquiryCachingService
from .persistence_service import PersistenceService

from .serializers import TwilioSMSSerializer
from .models import (
    SMSInquiry, 
    SMSFollowUpInquiry, 
    UnresolvedSMSInquiry,
    SMSInquiryResponse,
    SMSFollowUpResponse,
)


logger = logging.getLogger(__name__)


class SMSService:

    def __init__(self, msg: str, phone_number: str, message_sid: str):
        self.msg = msg
        self.phone_number = phone_number
        self.message_sid = message_sid
        self.resolver = self._get_resolver()
        self.sms_data: None | ResolvedSMS = None
        self.persistence_service: None | PersistenceService = None


    def _get_resolver(self) -> SMSResolver:
        return SMSResolver(msg=self.msg)

    def resolve(self) -> ResolvedSMS:
        return self.resolver.resolve_sms(
            message_sid=self.message_sid,
            phone_number=self.phone_number,
        )

    def geocode(self) -> Point | None:
        match self.sms_data.resolved_sms_type:
            case ResolvedSMSType.INQUIRY:
                location = self._get_location(location_str=self.sms_data.data.location_data.location)
            case ResolvedSMSType.FOLLOW_UP | ResolvedSMSType.UNRESOLVED | _:
                location = None        
        return location

    def save_sms(self, sms_data: ResolvedSMS, location:Point | None) -> IncomingSMSMessageModel:
        persistence_service = self._build_persistence_service(
            sms_data=sms_data, 
            location=location
        )
        persistence_service.save_sms()
        return persistence_service.instance


    def build_response_data(
            self, 
            instance: IncomingSMSMessageModel, 
    ) -> SMSInquiryResponseData | SMSFollowUpResponseData:
        response_service = ResponseService(instance)
        return response_service.build_response_data()


    def _build_persistence_service(self, sms_data:ResolvedSMS, location: Point | None) -> PersistenceService:
        return PersistenceService(sms_data=sms_data, location=location)

    def _get_location(self, location_str:str) -> Point:
        try:
            return GeocodingService.geocode(query=location_str)
        except Exception as e:
            logger.error(f"`{e.__class__.__name__}` occurred while attempting to geocode: {e}", exc_info=True)
            raise

    def save_response(self, response_data: SMSInquiryResponseData | SMSFollowUpResponseData):
        match self.sms_data.resolved_sms_type:
            case ResolvedSMSType.INQUIRY:
                self.persistence_service.save_inquiry_response(response_data=response_data)
            case ResolvedSMSType.FOLLOW_UP:
                self.persistence_service.save_follow_up_response(response_data=response_data)
            case ResolvedSMSType.UNRESOLVED:
                pass


    @classmethod
    def process_sms(cls, msg: str, phone_number: str, message_sid: str):
        sms_service = cls(msg=msg, phone_number=phone_number, message_sid=message_sid)
        sms_service.sms_data = sms_service.resolve()
        sms_location = sms_service.geocode()

        sms_service.persistence_service = sms_service._build_persistence_service(sms_data=sms_service.sms_data, location=sms_location)
        sms_service.persistence_service.save_sms()
        response_data = sms_service.build_response_data(instance=sms_service.persistence_service.instance)



        sms_service.save_response(response_data=response_data)
        wrapped_response_message = response_data.template.wrap_response(
            msg=response_data.msg,
            new_session=sms_service.persistence_service.new_session
        )
        print()
        print()
        print(wrapped_response_message)
        print()
        print()
        twiml = ...