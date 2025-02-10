import logging
from django.db import models
from sms.enums import SMSKeywordEnum, ResolvedSMSType

logger = logging.getLogger(__name__)


class BaseSMSMessageModel(models.Model):

    class Meta:
        abstract = True


class ResponseSMSMessageModel(BaseSMSMessageModel):

    class Meta:
        abstract = True

    @property
    def resource_ids_pretty(self) -> list[str|int]:
        return self.resource_ids if self.resource_ids is not None else "-"


class IncomingSMSMessageModel(BaseSMSMessageModel):

    class Meta:
        abstract = True


    @property
    def sms_type(self) -> ResolvedSMSType:
        match self._meta.model_name:
            case "smsinquiry":
                return ResolvedSMSType.INQUIRY
            case "smsfollowupinquiry":
                return ResolvedSMSType.FOLLOW_UP
            case "unresolvedsmsinquiry":
                return ResolvedSMSType.UNRESOLVED
            case _:
                msg = f"Unknown SMS type for record `{self.id}` in model `{self.__class__.__name__}`"
                logger.error(msg)
                raise TypeError(msg)

    def __str__(self) -> str:
       return self.message if len(self.message) <= 256 else f"{self.message[:253]}..." 
