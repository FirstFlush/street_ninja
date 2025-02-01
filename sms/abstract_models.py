from django.db import models


class BaseSMSMessageModel(models.Model):

    class Meta:
        abstract = True


class IncomingSMSMessageModel(BaseSMSMessageModel):

    class Meta:
        abstract = True