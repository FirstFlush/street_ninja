from abc import ABC, abstractmethod
import logging
from typing import Any
from sms.enums import SMSKeywordEnum
from .welcome_template import WelcomeTemplate

logger = logging.getLogger(__name__)


class BaseSMSResponseTemplate(ABC):

    TITLE = ""
    FOOTER = ""

    @classmethod
    def _convert_bool(cls, boolean: bool, abbreviated: bool = True) -> str:
        if isinstance(boolean, bool):
            if abbreviated:
                return "Y" if boolean else "N"
            else:
                return "Yes" if boolean else "No"
        msg = f"`{cls.__name__}`._convert_bool() Received invalid type for param boolean: `{type(boolean)}`, value `{boolean}`"
        logger.error(msg)
        raise TypeError(msg)


class GeneralResponseTemplate(BaseSMSResponseTemplate):

    def wrap_response(self, msg:str, new_session: bool = False) -> str:
        return msg


class QuerySetResponseTemplate(BaseSMSResponseTemplate):

    keyword_enum: SMSKeywordEnum | None = None
    FOOTER = "Reply 'MORE' for more results" 

    def __init__(self, params: dict[str, Any] | None = None):
        self.params = params

    @abstractmethod
    def format_result(self) -> str:
        ...

    def _params_string(self, sep: str = ", ") -> str:
        return sep.join([f"{k.capitalize()} {self._convert_bool(v, abbreviated=False) if isinstance(v, bool) else v}" for k, v in self.params.items()])

    def _params_pop(self, *keys: str):
        # NOTE not yet in use
        for key in keys:
            if self.params and self.params.get(key) is not None:
                self.params.pop(key)

    def distance(self, km: float) -> str:
        km = f"{round(km,1)}".rstrip("0").rstrip(".")
        return f"{km}km"
    
    def wrap_response(self, msg:str, new_session: bool = False) -> str:
        if new_session:
            top = f"{WelcomeTemplate.welcome_header()}\n\n{self.TITLE}"
            bottom = f"{WelcomeTemplate.WELCOME_FOOTER}"
            wrapped_msg = f"{top}\n{msg}\n{bottom}"
        else:
            top = self.TITLE
            bottom = f"{self.FOOTER}"
            wrapped_msg = f"{top}\n{msg}\n\n{bottom}\n"

        return wrapped_msg

