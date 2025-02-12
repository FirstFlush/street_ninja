import logging
import random
from .base_response_templates import BaseSMSResponseTemplate
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class HelpResponseTemplate(BaseSMSResponseTemplate):
    ...


class DirectionsResponseTemplate(BaseSMSResponseTemplate):
    ...



class InfoResponseTemplate(BaseSMSResponseTemplate):
    ...

