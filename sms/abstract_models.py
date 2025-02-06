import logging
from django.db import models
from common.enums import SMSKeywordEnum


logger = logging.getLogger(__name__)


class BaseSMSMessageModel(models.Model):

    class Meta:
        abstract = True


class IncomingSMSMessageModel(BaseSMSMessageModel):

    class Meta:
        abstract = True

    @property
    def keyword_enum(self) -> SMSKeywordEnum:
        try:
            return SMSKeywordEnum(self.keyword)
        except ValueError as e:
            msg = f"Invalid self.keyword `{self.keyword}` for sms model `{self.__class__.__name__}`"
            logger.error(msg, exc_info=True)
            raise            



    def __str__(self) -> str:
       return self.message if len(self.message) <= 256 else f"{self.message}..." 
