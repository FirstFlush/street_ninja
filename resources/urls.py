from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path("map/", MapView.as_view(), name='map'),  # /api/resources
]
