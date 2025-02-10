from django.contrib import admin
from street_ninja_server.base_admin import BaseGISAdmin
from sms.models import (
    PhoneNumber,
    Conversation,
    SMSInquiry,
    SMSFollowUpInquiry,
    UnresolvedSMSInquiry,
    SMSMessageOverflow,
    SMSInquiryResponse,
    SMSFollowUpResponse
)


class SMSInquiryInline(admin.TabularInline):
    model = SMSInquiry
    extra = 0
    readonly_fields = ("keyword", "location_text", "language", "message", "params_pretty", "location_pretty", "date_created")
    fields = ("keyword", "location_text", "location_pretty", "params_pretty", "language", "date_created")


class SMSFollowUpInline(admin.TabularInline):
    model = SMSFollowUpInquiry
    extra = 0
    readonly_fields = ("id", "keyword", "params_pretty", "message", "date_created")
    fields = ("id", "keyword", "params_pretty", "date_created")


class UnresolvedSMSInline(admin.TabularInline):
    model = UnresolvedSMSInquiry
    extra = 0
    readonly_fields = ("id", "message", "date_created")


class SMSInquiryResponseInline(admin.TabularInline):
    model = SMSInquiryResponse
    extra = 0
    readonly_fields = ("sms_inquiry", "resource_ids", "date_created")
    fields = ("sms_inquiry", "resource_ids", "date_created")


class SMSFollowUpResponseInline(admin.TabularInline):
    model = SMSFollowUpResponse
    extra = 0
    readonly_fields = ("sms_follow_up", "resource_ids_pretty", "date_created",)
    fields = ("sms_follow_up", "resource_ids_pretty", "date_created",)


class SMSMessageOverflowInline(admin.TabularInline):
    model = SMSMessageOverflow
    extra = 0
    readonly_fields = ("message", "date_created")


@admin.register(PhoneNumber)
class PhoneNumberAdmin(BaseGISAdmin):
    list_display = ("number", "last_active", "date_created")
    search_fields = ("number",)
    ordering = ("-date_created",)


@admin.register(Conversation)
class ConversationAdmin(BaseGISAdmin):
    list_display = ("id", "phone_number", "status", "date_created", "last_updated")
    search_fields = ("phone_number__number",)
    list_filter = ("status",)
    ordering = ("-last_updated",)
    inlines = [SMSInquiryInline, SMSFollowUpInline, UnresolvedSMSInline, SMSInquiryResponseInline, SMSFollowUpResponseInline]


@admin.register(SMSInquiry)
class SMSInquiryAdmin(BaseGISAdmin):
    list_display = ("conversation", "keyword", "location_text", "language", "message", "date_created")
    search_fields = ("conversation__phone_number__number", "keyword", "location_text", "message")
    list_filter = ("keyword", "language")
    ordering = ("-date_created",)
    inlines = [SMSMessageOverflowInline]


@admin.register(SMSFollowUpInquiry)
class SMSFollowUpInquiryAdmin(BaseGISAdmin):
    list_display = ("conversation", "keyword", "message", "date_created")
    search_fields = ("conversation__phone_number__number", "keyword", "message")
    list_filter = ("keyword",)
    ordering = ("-date_created",)


@admin.register(UnresolvedSMSInquiry)
class UnresolvedSMSInquiryAdmin(BaseGISAdmin):
    list_display = ("conversation", "message", "date_created")
    search_fields = ("conversation__phone_number__number", "message")
    ordering = ("-date_created",)


@admin.register(SMSMessageOverflow)
class SMSMessageOverflowAdmin(BaseGISAdmin):
    list_display = ("sms_inquiry", "sms_followup", "message", "date_created")
    search_fields = ("sms_inquiry__message", "sms_followup__message", "message")
    ordering = ("-date_created",)


@admin.register(SMSInquiryResponse)
class SMSInquiryResponseAdmin(BaseGISAdmin):
    list_display = ("conversation", "sms_inquiry", "resource_ids", "date_created")
    search_fields = ("conversation__phone_number__number",)
    ordering = ("-date_created",)


@admin.register(SMSFollowUpResponse)
class SMSFollowUpResponseAdmin(BaseGISAdmin):
    list_display = ("conversation", "sms_follow_up", "resource_ids_pretty", "date_created")
    search_fields = ("conversation__phone_number__number",)
    ordering = ("-date_created",)
