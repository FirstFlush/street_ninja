import logging
from django.contrib.gis.geos import Point
from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS, 
)
# from sms.response.respones_templates import ResourceResponseTemplate
from sms.response import (
    QuerySetResponseService, 
    InstanceResponseService, 
    SMSInquiryResponseData, 
    SMSFollowUpResponseData,
)
from sms.enums import ResolvedSMSType
from geo.geocoding import GeocodingService
from .abstract_models import IncomingSMSMessageModel
from cache.follow_up_service import FollowUpCachingService
from cache.inquiry_caching_service import InquiryCachingService
from .persistence_service import PersistenceService
from .resolvers.exc import SMSResolutionError
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

    def build_response_data(
            self, 
            instance: SMSInquiry | SMSFollowUpInquiry | UnresolvedSMSInquiry
    ) -> SMSInquiryResponseData | SMSFollowUpResponseData:
        """
        Processes the inquiry and generates a response according to its type.

        Each type will produce a datatype with the information required for
        the persistence layer to create the SMS Response object, and the
        caching layer to update and necessary ephemeral data.
        """
        if isinstance(instance, SMSInquiry):
            response = self._build_inquiry_response_data(instance)
        elif isinstance(instance, SMSFollowUpInquiry):
            response = self._build_follow_up_response(instance)
        elif isinstance(instance, UnresolvedSMSInquiry):
            response = self._build_unresolved_response(instance)
        else:
            msg = f"Received invalid type for instance argument: `{type(instance)}`"
            logger.error(msg)
            raise TypeError(msg)
        return response 
    
    def _build_inquiry_response_data(self, instance: SMSInquiry) -> SMSInquiryResponseData:
        
        caching_service = InquiryCachingService.init(inquiry=instance)
        session_data = caching_service.get_phone_session()
        offset = session_data.offset if session_data is not None else 0
        qs = caching_service.get_resources_by_proximity()
        response_service = QuerySetResponseService(
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
        ...

    def _build_unresolved_response(self, instance: UnresolvedSMSInquiry):
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
        sms_service.build_response_data(instance=sms_instance)
