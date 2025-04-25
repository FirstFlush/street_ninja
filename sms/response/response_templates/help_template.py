import logging
from .base_response_templates import BaseSMSResponseTemplate


logger = logging.getLogger(__name__)


class HelpResponseTemplate(BaseSMSResponseTemplate):
    """230 chars on April 24, 2025"""
    HELP_HEADER = "Street Ninja gives quick help with food, shelter, toilets, WiFi & water."

    INSTRUCTION = "Text what you need + a location."

    EXAMPLES = (
        "Examples:",
        "FOOD 222 Main",
        "SHELTER 275 E Cordova",
        "TOILET Drake and Seymour",
    )

    PROMPT = "Try it now — what can we help you find?"


    @classmethod
    def help_msg(cls, msg: str | None=None) -> str:
        examples = '\n'.join(cls.EXAMPLES)
        s = f"{cls.HELP_HEADER}\n\n{cls.INSTRUCTION}\n\n{examples}\n\n{cls.PROMPT}"
        if msg:
            return f"{msg}\n\n{s}"
        return s
