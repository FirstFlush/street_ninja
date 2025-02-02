from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path("all/", AllResourcesView.as_view(), name='resources_all'),  # /api/resources
]
