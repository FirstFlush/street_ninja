from django.contrib import admin
from .models import *


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'last_active', 'date_created')
    search_fields = ('number',)
    list_filter = ('last_active',)
    ordering = ('-date_created',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'status', 'keyword', 'message', 'date_created')
    search_fields = ('phone_number__number', 'message', 'keyword')
    list_filter = ('status', 'keyword')
    ordering = ('-date_created',)


@admin.register(RejectedInquiry)
class RejectedInquiryAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'message', 'date_created')
    search_fields = ('phone_number__number', 'message')
    ordering = ('-date_created',)


@admin.register(InquiryResponse)
class InquiryResponseAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'inquiry', 'message', 'date_created')
    search_fields = ('phone_number__number', 'inquiry__message', 'message')
    ordering = ('-date_created',)
