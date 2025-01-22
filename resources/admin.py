from django.contrib.gis import admin as gis_admin
from django.contrib import admin
from .models import Shelter


@admin.register(Shelter)
class ShelterAdmin(gis_admin.GISModelAdmin):

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
    # readonly_fields = ('date_created',)

    # Customize the map widget for the PointField
    map_template = 'gis/admin/openlayers.html'
    default_lon = -123.116226  # Example: Vancouver longitude
    default_lat = 49.246292   # Example: Vancouver latitude
    default_zoom = 12

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in self.model._meta.fields]
        return []
