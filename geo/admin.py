from django.contrib import admin
from street_ninja_server.base_admin import BaseAdmin, BaseGISAdmin
from .models import Location, InquiryCount


@admin.register(Location)
class LocationAdmin(BaseGISAdmin):
    list_display = ("id", "location_text", "location_type", "location", "date_last")


@admin.register(InquiryCount)
class InquiryCountAdmin(BaseAdmin):
    list_display = ("id", "location", "timestamp")
    search_fields = ("location__location_text",)