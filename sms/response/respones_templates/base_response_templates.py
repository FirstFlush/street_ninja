from abc import ABC, ABCMeta
from dataclasses import dataclass
from sms.enums import SMSKeywordEnum
from resources.abstract_models import ResourceModel

@dataclass
class BaseSMSResponseTemplate(ABC):
    ...


@dataclass
class ResourceResponseTemplate(BaseSMSResponseTemplate, metaclass=ABCMeta):

    keyword_enum: SMSKeywordEnum | None = None
    always_show: list[str] | None = None
    optional_params: list[str] | None = None
    response_format: str | None = None


@dataclass
class FollowUpResponseTemplate(BaseSMSResponseTemplate):
    ...

