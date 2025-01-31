from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path(settings.ROUTE_SMS_GATEWAY, SMSWebhookView.as_view(), name='sms_webhook'),  # /api/sms
]
