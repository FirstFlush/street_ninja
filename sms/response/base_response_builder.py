from abc import ABC, abstractmethod
import logging
from twilio.twiml.messaging_response import MessagingResponse
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceQuerySet, ResourceModel
from .respones_templates.resource_templates import (
    ShelterResponseTemplate,
    FoodResponseTemplate,
)
from .respones_templates import BaseSMSResponseTemplate


logger = logging.getLogger(__name__)


class BaseResponseBuilder(ABC):
    
    MAPPING = None
    keyword_enum = None

    def __init__(self):
        if self.MAPPING is None or self.keyword_enum is None:
            raise NotImplementedError(f"{self.__class__.__name__} must define self.MAPPING and self.keyword_enum")

    def _get_template(self) -> BaseSMSResponseTemplate:
        try:
            self.template = self.MAPPING[self.keyword_enum]
        except KeyError:
            msg = f"keyword_enum {self.keyword_enum} not found in {self.__class__.__name__}'s MAPPING attribute."
            logger.error(msg, exc_info=True)
            raise

    def to_twiml(self, msg: str) -> str:
        """
        Converts the response text to TwiML, a type of XML that Twilio Gateway requires.
        """
        mr = MessagingResponse()
        mr.message(msg)
        logger.info("Created TwiML response")
        return str(mr)
