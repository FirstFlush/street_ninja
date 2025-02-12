import logging
import random
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class WelcomeTemplate:
    """
    This class handles a presentation-layer wrapper that appears only on new conversations aka new sessions.
    This gives users context about how to interact with Street Ninja without repeating the context on every response.
    """
    EXAMPLE_LOCATIONS = [
        "275 Cordova St E",  # jail lol
        "222 Main St",
        "main st & hastings",
        "8384 granville st",
    ]

    _HEADER = """
🥷 Welcome to Street Ninja!

Get help fast: FOOD, SHELTER, TOILET, WIFI, WATER.
"""

    WELCOME_FOOTER = """
More results? Reply 'MORE'
Need details? Reply '[NUMBER] INFO'
Need directions? Reply '[NUMBER] DIRECTIONS'
Need help? Reply 'HELP'
"""

    @classmethod
    def _example(cls) -> str:
        try:
            example = f"{random.choice(SMSKeywordEnum.values).upper()} {random.choice(cls.EXAMPLE_LOCATIONS)}"
        except Exception as e:
            msg = f"Wtf? Error `{e.__class__.__name__}` occured while trying to build query example in `{cls.__name__}`. Error: {e}"
            logger.error(msg, exc_info=True)
            example = "275 Cordova St E"
        return f"(Example: {example})"


    @classmethod
    def welcome_header(cls) -> str:
        return f"{cls._HEADER}\n{cls._example()}"
