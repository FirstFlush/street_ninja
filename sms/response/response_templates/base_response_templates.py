from abc import ABC, abstractmethod
import logging
from typing import Any
from sms.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class BaseSMSResponseTemplate(ABC):

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


class QuerySetResponseTemplate(BaseSMSResponseTemplate):

    keyword_enum: SMSKeywordEnum | None = None
    FOOTER = "Reply 'MORE' for more results" 
    TITLE = ""

    def __init__(self, params: dict[str, Any] | None = None):
        self.params = params

    def _params_string(self, sep: str = ", ") -> str:
        return sep.join([f"{k.capitalize()} {self._convert_bool(v, abbreviated=False) if isinstance(v, bool) else v}" for k, v in self.params.items()])

    def distance(self, km: float) -> str:
        km = f"{round(km,1)}".rstrip("0").rstrip(".")
        return f"{km}km"
    
    @abstractmethod
    def format_result(self) -> str:
        ...

