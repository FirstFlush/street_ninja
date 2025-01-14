from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('inquiry', SMSInquiryView.as_view(), name='sms_inquiry'),
]
