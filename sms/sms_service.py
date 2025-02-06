import logging
from django.contrib.gis.geos import Point
from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS, 
    ResolvedSMSType,
)
from geo.geocoding import GeocodingService
from sms.persistence_service import PersistenceService
from sms.resolvers.exc import SMSResolutionError
from sms.serializers import TwilioSMSSerializer


logger = logging.getLogger(__name__)


class SMSService:

    def __init__(self, msg: str, phone_number: str, message_sid: str):
        self.resolver = SMSResolver(msg=msg)
        self.sms_data = self.resolver.resolve_sms(
            message_sid=message_sid,
            phone_number=phone_number,
        )
        match self.sms_data.resolved_sms_type:
            case ResolvedSMSType.INQUIRY:
                self.location = self._get_location()
            case _:
                self.location = None
        self.save_sms()



    def save_sms(self):
        persistence_service = self._build_persistence_service()
        persistence_service.save_sms()

    def handle_inquiry(self):
        ...




    def handle_follow_up(self):
        ...


        # match self.sms_data.resolved_sms_type:
        #     case ResolvedSMSType.INQUIRY:
        #         ...
        #     case ResolvedSMSType.FOLLOW_UP:
        #         follow_up_service = self._build_follow_up_service()



 
    def _build_persistence_service(self) -> PersistenceService:
        return PersistenceService(sms_data=self.sms_data, location=self.location)


    def _get_location(self) -> Point:
        try:
            return GeocodingService.geocode(query=self.sms_data.data.location_data.location)
        except Exception as e:
            logger.error(f"`{e.__class__.__name__}` occurred while attempting to geocode: {e}", exc_info=True)
            raise