from datetime import datetime, timedelta, timezone
import uuid
from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from common.enums import (
    SMSKeywordEnum, 
    LanguageEnum, 
    InquiryStatusEnum, 
    LocationType
)
from sms.enums import ConversationStatus, SMSFollowUpKeywordEnum
from sms.resolvers import ResolvedSMSFollowUp, ResolvedSMSInquiry
from .abstract_models import IncomingSMSMessageModel, BaseSMSMessageModel


class PhoneNumber(models.Model):

    number = models.CharField(max_length=20, unique=True)
    last_active = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.number


class ConversationManager(models.Manager):

    def get_or_create_conversation(self, phone_number: str) -> "Conversation":
        """Retrieves an active conversation or creates a new one if none exist."""
        now = datetime.now(tz=timezone.utc)
        session_expiry = now - timedelta(minutes=settings.PHONE_SESSION_LENGTH)
        phone, _ = PhoneNumber.objects.get_or_create(number=phone_number, defaults={"last_active": now})
        conversation = self.filter(
            phone_number=phone, 
            date_updated__gte=session_expiry
        ).prefetch_related(
            "smsinquiry_set", "smsfollowupinquiry_set", "unresolvedsmsinquiry_set", "smsresponse_set"
        ).first()

        if conversation:
            return conversation

        return self.create(
            phone_number=phone,
            phone_session_key=Conversation.generate_phone_session_key(),
            date_created=now,
            date_updated=now,
        )


class Conversation(models.Model):
    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    phone_session_key = models.CharField(unique=True)
    status = models.CharField(choices=ConversationStatus.choices)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects:ConversationManager = ConversationManager()

    def __str__(self) -> str:
        return self.phone_session_key

    @staticmethod
    def generate_phone_session_key() -> str:
        """Generates a unique session key for a new conversation."""
        return str(uuid.uuid4())


class SMSInquiryManager(models.Manager):
    
    def save_inquiry_sms(
            self, 
            conversation: Conversation,
            location: Point,
            sms_data: ResolvedSMSInquiry
    )-> "SMSInquiry":
        return SMSInquiry.objects.create(
            conversation=conversation,
            keyword=sms_data.keyword_language_data.sms_keyword_enum.value,
            message=sms_data.msg,
            location=location,
            location_text=sms_data.location_data.location,
            location_type=sms_data.location_data.location_type.value,
            language=sms_data.keyword_language_data.language_enum.value,
            params=sms_data.params.to_dict(),
        )


class SMSInquiry(IncomingSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, choices=SMSKeywordEnum.choices)
    location = gis_models.PointField(srid=4326)
    location_text = models.CharField(max_length=256)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    language = models.CharField(max_length=3, choices=LanguageEnum.choices)
    message = models.CharField(max_length=256)
    params = models.JSONField(default=dict)
    date_created = models.DateTimeField(auto_now_add=True)

    objects: SMSInquiryManager = SMSInquiryManager()

    class Meta:
        verbose_name_plural = "Inquiries"

    @property
    def location_pretty(self) -> str:
        self.location:Point
        return f"[{round(self.location.x, 5)}, {round(self.location.y, 5)}]"


class SMSFollowUpInquiryManager(models.Manager):

    def save_follow_up_sms(self, conversation: Conversation, sms_data:ResolvedSMSFollowUp)-> "SMSFollowUpInquiry":
        return SMSFollowUpInquiry.objects.create(
            conversation=conversation,
            message=sms_data.msg,
            keyword=sms_data.follow_up_keyword_enum.value,
            params=sms_data.follow_up_params,
        )


class SMSFollowUpInquiry(IncomingSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, choices=SMSFollowUpKeywordEnum.choices)
    message = models.CharField(max_length=256)
    params = models.JSONField(default=dict)
    date_created = models.DateTimeField(auto_now_add=True)

    objects:SMSFollowUpInquiryManager = SMSFollowUpInquiryManager()

    class Meta:
        verbose_name_plural = "Follow-up inquiries"


class UnresolvedSMSInquiryManager(models.Manager):

    def save_unresolved_sms(self, conversation: Conversation, message: str) -> "UnresolvedSMSInquiry":
        return UnresolvedSMSInquiry.objects.create(
            conversation=conversation,
            message=message,
        )
    

class UnresolvedSMSInquiry(IncomingSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)

    objects:UnresolvedSMSInquiryManager = UnresolvedSMSInquiryManager()

    class Meta:
        verbose_name_plural = "Unresolved SMS Inquiries"


class SMSMessageOverflow(models.Model):
    sms_inquiry = models.ForeignKey(to=SMSInquiry, on_delete=models.CASCADE, null=True)
    sms_followup = models.ForeignKey(to=SMSFollowUpInquiry, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)




class SMSResponse(BaseSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

