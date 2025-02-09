import logging
from django.contrib.gis.geos import Point
from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS, 
)
# from sms.response.respones_templates import ResourceResponseTemplate
from sms.response import QuerySetResponseService, InstanceResponseService
from sms.enums import ResolvedSMSType
from geo.geocoding import GeocodingService
from .abstract_models import IncomingSMSMessageModel
from cache.follow_up_service import FollowUpCachingService
from cache.inquiry_service import InquiryCachingService
from .persistence_service import PersistenceService
from .resolvers.exc import SMSResolutionError
from .serializers import TwilioSMSSerializer
from .models import SMSInquiry, SMSFollowUpInquiry, UnresolvedSMSInquiry


logger = logging.getLogger(__name__)


class SMSService:

    def __init__(self, msg: str, phone_number: str, message_sid: str):
        self.msg = msg
        self.phone_number = phone_number
        self.message_sid = message_sid
        self.resolver = self._get_resolver()



    def _get_resolver(self) -> SMSResolver:
        return SMSResolver(msg=self.msg)


    def resolve(self) -> ResolvedSMS:
        return self.resolver.resolve_sms(
            message_sid=self.message_sid,
            phone_number=self.phone_number,
        )

    def geocode(self, sms_data: ResolvedSMS) -> Point | None:
        match sms_data.resolved_sms_type:
            case ResolvedSMSType.INQUIRY:
                location = self._get_location(location_str=sms_data.data.location_data.location)
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


    def prepare_response(self, instance: SMSInquiry | SMSFollowUpInquiry | UnresolvedSMSInquiry):
        if isinstance(instance, SMSInquiry):
            self._process_inquiry(instance)
        elif isinstance(instance, SMSFollowUpInquiry):
            self._process_follow_up()
        elif isinstance(instance, UnresolvedSMSInquiry):
            self._process_unresolved()
        else:
            msg = f"Received invalid type for instance argument: `{type(instance)}`"
            logger.error(msg)
            raise TypeError(msg)
    

    def _process_inquiry(self, instance: SMSInquiry):
        
        caching_service = InquiryCachingService.init(inquiry=instance)
        qs = caching_service.get_resources_by_proximity()
        response_service = QuerySetResponseService(queryset=qs)        
        response = response_service.create_response()
        print(response)
        # caching_service.get_phone_session()

    def _process_follow_up(self, instance: SMSFollowUpInquiry):
        ...


    def _process_unresolved(self, instance: UnresolvedSMSInquiry):
        ...


    def _build_persistence_service(self, sms_data:ResolvedSMS, location: Point | None) -> PersistenceService:
        return PersistenceService(sms_data=sms_data, location=location)


    def _get_location(self, location_str:str) -> Point:
        try:
            return GeocodingService.geocode(query=location_str)
        except Exception as e:
            logger.error(f"`{e.__class__.__name__}` occurred while attempting to geocode: {e}", exc_info=True)
            raise


    @classmethod
    def process_sms(cls, msg: str, phone_number: str, message_sid: str):

        sms_service = cls(msg=msg, phone_number=phone_number, message_sid=message_sid)
        sms_data = sms_service.resolve()
        sms_location = sms_service.geocode(sms_data=sms_data)
        sms_instance = sms_service.save_sms(sms_data=sms_data, location=sms_location)
        sms_service.prepare_response(instance=sms_instance)
