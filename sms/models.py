from datetime import datetime, timedelta, timezone
import logging
from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from common.enums import (
    LanguageEnum, 
    LocationType,
)
from geo.models import Location
from sms.enums import ConversationStatus, SMSFollowUpKeywordEnum, SMSKeywordEnum
from sms.resolvers.follow_up_resolver import ResolvedSMSFollowUp
from sms.resolvers.dataclasses import ResolvedSMSInquiry
from .abstract_models import IncomingSMSMessageModel, ResponseSMSMessageModel


logger = logging.getLogger(__name__)


class PhoneNumber(models.Model):

    number = models.CharField(max_length=20, unique=True)
    last_active = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.number


class ConversationManager(models.Manager):

    def get_or_create_conversation(self, phone_number: PhoneNumber, now: datetime) -> tuple["Conversation", bool]:
        """
        Retrieves an active conversation for the given phone number. 
        If no active session exists within the TTL, creates a new conversation.
        """
        session_expiry = now - timedelta(seconds=settings.TTL_PHONE_SESSION)
        logger.info(f"session_expiry stringified: {session_expiry.strftime('%Y-%m-%d %H:%M:%S')}")
        conversation = self.filter(
            phone_number=phone_number, 
            last_updated__gte=session_expiry
        ).prefetch_related(
            "smsinquiry_set", "smsfollowupinquiry_set", "unresolvedsmsinquiry_set",
        ).first()

        if conversation:
            return conversation, False

        return self.create(
            phone_number=phone_number,
            date_created=now,
            last_updated=now,
        ), True


class Conversation(models.Model):
    phone_number = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE)
    status = models.CharField(choices=ConversationStatus.choices)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects:ConversationManager = ConversationManager()

    def __str__(self) -> str:
        return f"{self.phone_number} {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"


class SMSInquiryManager(models.Manager):
    
    def save_inquiry_sms(
            self, 
            conversation: Conversation,
            # location: Point,
            sms_data: ResolvedSMSInquiry,
            inquiry_location: Location,
    )-> "SMSInquiry":
        return SMSInquiry.objects.create(
            conversation=conversation,
            keyword=sms_data.keyword_language_data.sms_keyword_enum.value,
            message=sms_data.msg,
            # location=location,
            # location_text=sms_data.location_data.location,
            # location_type=sms_data.location_data.location_type.value,
            inquiry_location=inquiry_location,
            language=sms_data.keyword_language_data.language_enum.value,
            params=sms_data.params.to_dict(),
        )


class SMSInquiry(IncomingSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, choices=SMSKeywordEnum.choices)
    location = gis_models.PointField(srid=4326, null=True)
    location_text = models.CharField(max_length=256, null=True)
    location_type = models.CharField(max_length=20, choices=LocationType.choices, null=True)
    inquiry_location = models.ForeignKey(to=Location, on_delete=models.CASCADE, null=True)
    language = models.CharField(max_length=3, choices=LanguageEnum.choices)
    message = models.CharField(max_length=256)
    params = models.JSONField(default=dict)
    date_created = models.DateTimeField(auto_now_add=True)

    objects: SMSInquiryManager = SMSInquiryManager()

    class Meta:
        verbose_name_plural = "Inquiries"

    @property
    def keyword_enum(self) -> SMSKeywordEnum:
        try:
            return SMSKeywordEnum(self.keyword)
        except ValueError as e:
            msg = f"Invalid self.keyword `{self.keyword}` for record `{self.id}` in model `{self.__class__.__name__}` causing error: {e}"
            logger.error(msg, exc_info=True)
            raise            

    @property
    def location_pretty(self) -> str:
        self.location:Point
        return f"{round(self.location.x, 5)}, {round(self.location.y, 5)}"


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
    directions_text = models.TextField(null=True)
    params = models.JSONField(default=dict)
    date_created = models.DateTimeField(auto_now_add=True)

    objects:SMSFollowUpInquiryManager = SMSFollowUpInquiryManager()

    class Meta:
        verbose_name_plural = "Follow-up inquiries"

    @property
    def keyword_enum(self) -> SMSFollowUpKeywordEnum:
        try:
            return SMSFollowUpKeywordEnum(self.keyword)
        except ValueError as e:
            msg = f"Invalid self.keyword `{self.keyword}` for record `{self.id}` in model `{self.__class__.__name__}`"
            logger.error(msg, exc_info=True)
            raise         


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
    keyword = None

    class Meta:
        verbose_name_plural = "Unresolved SMS Inquiries"

    @property
    def keyword_enum(self) -> None:
        return None


class SMSMessageOverflow(models.Model):
    sms_inquiry = models.ForeignKey(to=SMSInquiry, on_delete=models.CASCADE, null=True)
    sms_followup = models.ForeignKey(to=SMSFollowUpInquiry, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class SMSInquiryResponse(ResponseSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    sms_inquiry = models.OneToOneField(to=SMSInquiry, on_delete=models.CASCADE)
    resource_ids = ArrayField(models.IntegerField())
    date_created = models.DateTimeField(auto_now_add=True)


class SMSFollowUpResponse(ResponseSMSMessageModel):
    conversation = models.ForeignKey(to=Conversation, on_delete=models.CASCADE)
    sms_follow_up = models.OneToOneField(to=SMSFollowUpInquiry, on_delete=models.CASCADE)
    resource_ids = ArrayField(models.IntegerField(), null=True)
    directions = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
