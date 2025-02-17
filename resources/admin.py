from django.contrib import admin
from street_ninja_server.base_admin import BaseAdmin, BaseGISAdmin
from .models import Shelter


@admin.register(Shelter)
class ShelterAdmin(BaseGISAdmin):

    list_display = (
        'facility',
        'address',
        'category',
        'phone',
        'meals',
        'pets',
        'carts',
        'last_fetched',
        'date_created',
    )
    list_filter = ('category', 'meals', 'pets', 'carts')
    search_fields = ('facility', 'address', 'phone')
    ordering = ('-last_fetched',)

    map_template = 'gis/admin/openlayers.html'
    default_lon = -123.116226  # Example: Vancouver longitude
    default_lat = 49.246292   # Example: Vancouver latitude
    default_zoom = 12
