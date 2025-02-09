import logging
from dataclasses import dataclass
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceModel


logger = logging.getLogger(__name__)


class BaseSMSResponseTemplate():
    
    @classmethod
    def format_response(cls, instance: ResourceModel):
        msg = f"`{cls.__name__}` must implement format_response() method!"
        logger.error(msg)
        raise NotImplementedError(msg)

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


class ResourceResponseTemplate(BaseSMSResponseTemplate):

    keyword_enum: SMSKeywordEnum | None = None
    always_show: list[str] | None = None
    optional_params: list[str] | None = None
    response_format: str | None = None


class FollowUpResponseTemplate(BaseSMSResponseTemplate):
    ...

