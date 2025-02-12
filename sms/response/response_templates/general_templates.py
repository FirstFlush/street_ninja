import logging
import random
from .base_response_templates import BaseSMSResponseTemplate
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class HelpResponseTemplate(BaseSMSResponseTemplate):
    ...


class WelcomeResponseTemplate(BaseSMSResponseTemplate):

    EXAMPLE_LOCATIONS = [
        '222 Main St',
        'main st & hastings',
        '8384 granville st',
        '275 Cordova St E',
    ]

    HEADER = """
🥷 Welcome to Street Ninja!

Get help fast: FOOD, SHELTER, TOILET, WIFI, WATER.

(Example: SHELTER 275 Cordova St E)

"""

    FOOTER = """

More results? Reply MORE.
Need details? Reply [NUMBER] INFO
Need directions? Reply [NUMBER] DIRECTIONS
Need help? Reply HELP

"""

    def build_example(self) -> str:
        try:
            return f"{random.choice(SMSKeywordEnum.choices).upper()} {random.choice(self.EXAMPLE_LOCATIONS)}"
        except Exception as e:
            msg = f"Wtf? Error `{e.__class__.__name__}` occured while trying to build query example in `{self.__class__.__name__}`. Error: {e}"
            logger.error(msg, exc_info=True)
            return "275 Cordova St E"


class DirectionsResponseTemplate(BaseSMSResponseTemplate):
    ...



class InfoResponseTemplate(BaseSMSResponseTemplate):
    ...

