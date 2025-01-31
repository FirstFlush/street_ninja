from django.db import models
from django.contrib.gis.db import models as gis_models
from common.enums import (
    SMSKeywordEnum, 
    LanguageEnum, 
    InquiryStatusEnum, 
    LocationType
)
from sms.enums import ConversationStatus, SMSFollowUpKeywordEnum


class PhoneNumber(models.Model):

    number = models.CharField(max_length=20, unique=True)
    last_active = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    phone_session_key = models.CharField(unique=True)
    status = models.CharField(choices=ConversationStatus.choices)
    date_created = models.DateTimeField(auto_now_add=True)


    # @staticmethod
    # get_phone_session_key


class SMSInquiry(models.Model):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, choices=SMSKeywordEnum.choices)
    location = gis_models.PointField(srid=4326)
    location_text = models.CharField(max_length=256)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    status = models.CharField(max_length=16, choices=InquiryStatusEnum.choices)
    language = models.CharField(max_length=3, choices=LanguageEnum.choices)
    message = models.CharField(max_length=256)
    params = models.JSONField(default=dict)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"


class SMSFollowUpInquiry(models.Model):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, choices=SMSFollowUpKeywordEnum.choices)
    message = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Follow-up inquiries"


class SMSMessageOverflow(models.Model):
    sms_inquiry = models.ForeignKey(to=SMSInquiry, on_delete=models.CASCADE, null=True)
    sms_followup = models.ForeignKey(to=SMSFollowUpInquiry, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class UnresolvedSMSInquiry(models.Model):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Unresolved SMS Inquiries"


class SMSResponse(models.Model):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

