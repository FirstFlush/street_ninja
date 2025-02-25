from abc import ABC
import logging


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



