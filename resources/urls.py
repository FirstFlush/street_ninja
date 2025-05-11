from django.urls import path
from .views import MapView, MapPinView

urlpatterns = [
    path("map/", MapView.as_view(), name='map'),            # /api/resources
    path("map/pin/<str:resourceType>/<int:id>/", MapPinView.as_view(), name='map_pin'),     # /api/resources
]
