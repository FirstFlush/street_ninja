from django.urls import path
from .views import *
from django.conf import settings

sms_gateway_route = getattr(settings, 'ROUTE_SMS_GATEWAY', 'sms-gateway/')
if sms_gateway_route is None:
    sms_gateway_route = 'sms-gateway/'

urlpatterns = [
    path(sms_gateway_route, SMSWebhookView.as_view(), name='sms_webhook'),
    path('web-query/', SMSWebsiteView.as_view(), name='sms_webhook'),
]
