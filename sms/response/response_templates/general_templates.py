import logging
import random
from .base_response_templates import BaseSMSResponseTemplate
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class HelpResponseTemplate(BaseSMSResponseTemplate):
    """602 characters"""
    HELP_HEADER = "🥷 Street Ninja Help 🥷"

    HELP_DESCRIPTION = "Street Ninja gives you quick info on essential resources nearby. Just text what you need along with your location, and get instant results. No sign-ups, no hassle."

    RESOURCES = (
        "📌 Resources:\n"
        "- FOOD → Find free meals nearby.\n"
        "- SHELTER → Get a list of shelters.\n"
        "- TOILET → Locate public restrooms.\n"
        "- WIFI → Find free WiFi spots.\n"
        "- WATER → Get drinking fountain locations."
    )

    EXAMPLE_QUERIES = (
        "📝 Example inquiries:\n"
        "SHELTER 275 Cordova St E\n"
        "FOOD Main and Hastings St\n"
        "WIFI Drake and Seymour\n"
        "mens shelter granville st & pender\n"
        "shelter for women with pets allowed 222 Main St"
    )

    PROMPT = "What can Street Ninja help you find today?"

    @classmethod
    def help_msg(cls) -> str:
        return f"{cls.HELP_HEADER}\n\n{cls.HELP_DESCRIPTION}\n\n{cls.RESOURCES}\n\n{cls.EXAMPLE_QUERIES}\n\n{cls.PROMPT}"

class DirectionsResponseTemplate(BaseSMSResponseTemplate):
    ...



class InfoResponseTemplate(BaseSMSResponseTemplate):
    ...

