from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import *

admin.site.site_header = "Street Ninja Admin Panel"
admin.site.site_title = "Street Ninja"
admin.site.index_title = "Street Ninja"

admin_route = getattr(settings, "ROUTE_ADMIN", "admin/")
if admin_route is None:
    admin_route = "admin/"

urlpatterns = [
    path(admin_route, admin.site.urls),
    path('contact/', include('contacts.urls')),
    path('ping/', PingView.as_view(), name="ping"),
    path('resources/', include('resources.urls')),
    path('sms/', include('sms.urls')),
    path('scratch/', ScratchView.as_view(), name="scratch"),     # route used for quick testing
]
