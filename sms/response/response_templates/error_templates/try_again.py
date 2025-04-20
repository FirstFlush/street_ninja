from .base_error import BaseErrorResponseTemplate
import random


class TryAgainResponseTemplate(BaseErrorResponseTemplate):

    PROMPTS = [
        "Hmm, didn't catch that.",
        "Not sure what you’re looking for.",
        "Let’s try that again.",
        "That didn’t come through clearly.",
    ]

    TIP = (
        "Try sending a keyword like FOOD or SHELTER plus your location.\n"
        "Example: FOOD 222 Main St"
    )

    HELP_HINT = "Text HELP anytime to see more examples."

    @classmethod
    def msg(cls, msg: str | None=None) -> str:
        header = random.choice(cls.PROMPTS)
        s = f"{header}\n\n{cls.TIP}\n\n{cls.HELP_HINT}"
        if msg:
            return f"{msg}\n\n{s}"
        return s
