import logging
from django.contrib.gis.geos import Point
from django.contrib.sessions.backends.base import SessionBase
from sms.resolvers import (
    SMSResolver, 
    ResolvedSMS,
    SMSResolutionError
)
from sms.response import (
    SMSInquiryResponseData, 
    SMSFollowUpResponseData,
    ResponseService,
)
from sms.persistence_service import PersistenceService
from sms.enums import ResolvedSMSType
from geo.geocoding.geocoding_service import GeocodingService
from geo.geocoding.exc import AllGeocodersFailed
from geo.location_service import LocationService
from geo.models import Location
from notifications.tasks import send_geocoding_failed_email, send_sms_resolution_failed_email
from .abstract_models import IncomingSMSMessageModel, ResponseSMSMessageModel
from .response.response_templates.help_template import HelpResponseTemplate
from .persistence_service import PersistenceService
from .web.sms_web_service import SMSWebService


logger = logging.getLogger(__name__)


class SMSService:

    def __init__(
            self, msg: str, 
            phone_number: str, 
            message_sid: str | None = None
    ):
        self.msg = msg
        self.phone_number = phone_number
        self.message_sid = message_sid
        self.resolver = self._get_resolver()
        self.sms_data: None | ResolvedSMS = None
        self.persistence_service: None | PersistenceService = None
        self.response_service: None | ResponseService = None

    def _get_resolver(self) -> SMSResolver:
        return SMSResolver(msg=self.msg)

    def _resolve(self) -> ResolvedSMS:
        try:
            return self.resolver.resolve_sms(
                message_sid=self.message_sid,
                phone_number=self.phone_number,
            )
        except SMSResolutionError:
            logger.error("SMS Resolution failed! Sending email notification...", exc_info=True)
            send_sms_resolution_failed_email.delay(self.msg)
            raise

    def _geocode(self) -> Point | None:
        match self.sms_data.resolved_sms_type:
            case ResolvedSMSType.INQUIRY:
                location = self._get_geocoded_location(location_str=self.sms_data.data.location_data.location)
            case ResolvedSMSType.FOLLOW_UP | ResolvedSMSType.UNRESOLVED | _:
                location = None
        return location

    def _set_persistence_service(
            self, sms_data: ResolvedSMS,
            inquiry_location: Location | None
    ):
        self.persistence_service =  PersistenceService(
            sms_data=sms_data,
            inquiry_location=inquiry_location
        )

    def save_sms(self, sms_data: ResolvedSMS, inquiry_location: Location | None) -> IncomingSMSMessageModel:
        self._set_persistence_service(
            sms_data=sms_data, 
            inquiry_location=inquiry_location,
        )
        self.persistence_service.save_sms()
        return self.persistence_service.instance


    def _get_geocoded_location(self, location_str:str) -> Point:
        try:
            return GeocodingService.geocode(query=location_str)
        except AllGeocodersFailed:
            logger.error(f"All Geocoders failed. sending email notification...", exc_info=True)
            send_geocoding_failed_email.delay(self.msg)
            raise

        except Exception as e:
            logger.error(f"`{e.__class__.__name__}` occurred while attempting to geocode: {e}", exc_info=True)
            raise

    def save_response(self, response_data: SMSInquiryResponseData | SMSFollowUpResponseData) -> ResponseSMSMessageModel | None:
        match self.sms_data.resolved_sms_type:
            case ResolvedSMSType.INQUIRY:
                return self.persistence_service.save_inquiry_response(response_data=response_data)
            case ResolvedSMSType.FOLLOW_UP:
                return self.persistence_service.save_follow_up_response(response_data=response_data)
            case ResolvedSMSType.UNRESOLVED:
                return None
            case _:
                msg = f"`{self.__class__.__name__}` save_response() method received invalid ResolveSMSType enum: `{self.sms_data.resolved_sms_type}`"
                logger.error(msg)
                raise TypeError(msg)


    def _set_response_service(self, sms_instance: IncomingSMSMessageModel):
        try:
            response_service = ResponseService(instance=sms_instance)
        except Exception as e:
            logger.error(f"{e.__class__.__name__} while building response service: {e}")
        else:
            self.response_service = response_service


    def _get_location(self) -> Location:
        location_service = LocationService()
        location_id = location_service.check_mapping(
            location_text=self.sms_data.data.location_data.location
        )
        if location_id is not None:
            location = location_service.get_location(id=location_id)
        else:
            logger.info(f"No location id found in location cache. Creating new Location instance...")
            point = self._geocode()
            location = location_service.new_location(
                resolved_location=self.sms_data.data.location_data,
                point=point,
            )
        return location

    @classmethod
    def process_web_sms(cls, msg: str, session: SessionBase) -> str:
        sms_web_service = SMSWebService.init(query=msg, session=session)
        phone_number = sms_web_service.get_phone_number()
        try:
            return cls.process_sms(msg=msg, phone_number=phone_number) 
        except Exception as e:
            msg = f"Unexpected exception `{e.__class__.__name__}`when calling process_sms from the process_web_sms method: {e}"
            logger.error(msg)
            raise

    def _build_response(self) -> SMSInquiryResponseData | SMSFollowUpResponseData | None:
        if self.response_service is None:
            msg = "SMSService.response_service is None! Can not build response."
            logger.error(msg)
            raise RuntimeError(msg)
        else:
            try:
                return self.response_service.build_response_data()
            except Exception as e:
                logger.error(f"{e.__class__.__name__} while building response data: {e}")
        return None


    def _render_response(self, response_data: SMSInquiryResponseData | SMSFollowUpResponseData) -> str:
        response_instance = self.save_response(response_data=response_data)
        if response_instance:
            wrapped_response_message = response_data.template.wrap_response(
                msg=response_data.msg,
                new_session=self.persistence_service.new_session,
            )
        else:
            wrapped_response_message = self.response_service.build_help_msg()
            
        return wrapped_response_message


    def _sms_intake(self) -> IncomingSMSMessageModel:
        """
        Resolves the incoming SMS message, performs geocoding (if required),
        and saves the inquiry and related metadata to the database.

        This method orchestrates the first half of the SMS processing flow:
        - Parsing and resolving keyword, filters, and location text
        - Looking up or geocoding the physical location
        - Persisting the parsed SMS and location data
        """
        self.sms_data = self._resolve()
        try:
            if self.sms_data.resolved_sms_type == ResolvedSMSType.INQUIRY:
                location = self._get_location()
            else:
                location = None
        except Exception as e:
            logger.error(f"Unexpected error `{e.__class__.__name__}` while parsing location: {e}")

        return self.save_sms(
            sms_data=self.sms_data, 
            # location=location.location if location is not None else None,
            inquiry_location=location,
        )

    def _sms_response(self, sms_instance: IncomingSMSMessageModel):
        """
        Orchestrates the second half of the SMS processing flow by 
        generating and formatting the final response message.

        This method:
        - Initializes the response service using the saved SMS instance
        - Builds the response content based on the resolved SMS data
        - Renders the final response string using the appropriate template

        If response generation fails, a default help message is returned.
        """
        self._set_response_service(sms_instance)
        response_data = self._build_response()
        if response_data is None:
            return HelpResponseTemplate.help_msg()
        else:
            return self._render_response(
                response_data=response_data,
            )

    @classmethod
    def process_sms(
            cls, 
            msg: str, 
            phone_number: str, 
            message_sid: str|None=None
    ) -> str:
        """"Primary orchestration method for the entire app."""
        sms_service = cls(msg=msg, phone_number=phone_number, message_sid=message_sid)
        sms_instance = sms_service._sms_intake()
        return sms_service._sms_response(sms_instance)

