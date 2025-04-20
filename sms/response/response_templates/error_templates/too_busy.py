from .base_error import BaseErrorResponseTemplate


class TooBusyResponseTemplate(BaseErrorResponseTemplate):
    PROMPT = (
        "🥷 We're getting a lot of requests right now.\n\n"
        "Street Ninja’s a bit backed up — please try again in a few minutes."
    )

    @classmethod
    def msg(cls, msg: str | None=None) -> str:
        if msg:
            return f"{msg}\n\n{cls.PROMPT}"
        return cls.PROMPT
