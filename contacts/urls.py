from django.urls import path
from .views import *

urlpatterns = [
    path('', ContactView.as_view(), name='contact'), 
]
