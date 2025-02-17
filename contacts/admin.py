from django.contrib import admin
from street_ninja_server.base_admin import BaseAdmin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ("id", "name", "organization", "email", "phone", "contactMethod", "date_created")
    list_filter = ("contactMethod", "date_created")
    search_fields = ("name", "email", "phone", "organization", "msg")
