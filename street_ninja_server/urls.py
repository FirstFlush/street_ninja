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
    # path('', HomeView.as_view(), name='home'),
    # path('keywords/', KeywordTestView.as_view(), name='keyword_test'),
    # path('redis/', RedisTestView.as_view(), name='redis_test'),
    # path('directions/', DirectionsView.as_view(), name='directions'),
    path('api/test/', TestView.as_view(), name="test"),
    path('api/contact/', include('contacts.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/sms/', include('sms.urls')),
]
