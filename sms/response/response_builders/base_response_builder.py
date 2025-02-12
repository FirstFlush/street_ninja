from abc import ABC
import logging
from twilio.twiml.messaging_response import MessagingResponse
from sms.enums import SMSKeywordEnum
from ..response_templates import BaseSMSResponseTemplate


logger = logging.getLogger(__name__)


class BaseResponseBuilder(ABC):

    def __init__(self):
        ...


    # def to_twiml(self, msg: str) -> str:
    #     """
    #     Converts the response text to TwiML, a type of XML that Twilio Gateway requires.
    #     """
    #     mr = MessagingResponse()
    #     mr.message(msg)
    #     logger.info("Created TwiML response")
    #     return str(mr)
