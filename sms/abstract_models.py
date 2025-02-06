from django.db import models


class BaseSMSMessageModel(models.Model):

    class Meta:
        abstract = True


class IncomingSMSMessageModel(BaseSMSMessageModel):

    class Meta:
        abstract = True

    def __str__(self) -> str:
       return self.message if len(self.message) <= 256 else f"{self.message}..." 
