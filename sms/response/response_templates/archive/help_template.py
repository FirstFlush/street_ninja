import logging
from .base_response_templates import BaseSMSResponseTemplate


logger = logging.getLogger(__name__)


class HelpResponseTemplate(BaseSMSResponseTemplate):
    """602 characters"""
    HELP_HEADER = "Street Ninja Help"

    HELP_DESCRIPTION = "Street Ninja gives you quick info on essential resources nearby. Just text what you need along with your location, and get instant results."

    RESOURCES = (
        "Resources:\n"
        "- FOOD Find free meals nearby.\n"
        "- SHELTER Get a list of shelters.\n"
        "- TOILET Locate public restrooms.\n"
        "- WIFI Find free WiFi spots.\n"
        "- WATER Get drinking fountain locations."
    )

    EXAMPLE_QUERIES = (
        "Examples:\n"
        "SHELTER 275 Cordova St E\n"
        "FOOD Main and Hastings St\n"
        "WIFI Drake and Seymour\n"
        "womens shelter granville st & pender\n"
        "shelter pets-friendly 222 Main St"
    )

    PROMPT = "What can Street Ninja help you find today?"

    @classmethod
    def help_msg(cls, msg: str | None=None) -> str:
        s = f"{cls.HELP_HEADER}\n\n{cls.HELP_DESCRIPTION}\n\n{cls.RESOURCES}\n\n{cls.EXAMPLE_QUERIES}\n\n{cls.PROMPT}"
        if msg:
            return f"{msg}\n\n{s}"
        return s
