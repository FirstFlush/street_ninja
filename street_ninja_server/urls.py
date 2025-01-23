from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import *

admin.site.site_header = "Street Ninja Admin Panel"
admin.site.site_title = "Street Ninja"
admin.site.index_title = "Street Ninja"

urlpatterns = [
    path(settings.ROUTE_ADMIN, admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('keywords/', KeywordTestView.as_view(), name='keyword'),
    path('sms/', include('sms.urls')),
]
