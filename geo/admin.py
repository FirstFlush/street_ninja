from django.contrib import admin
from street_ninja_server.base_admin import BaseAdmin, BaseGISAdmin
from .models import Location, Neighborhood


@admin.register(Location)
class LocationAdmin(BaseGISAdmin):
    list_display = ("id", "location_text", "location_type", "location", "date_last")


@admin.register(Neighborhood)
class NeighborhoodAdmin(BaseGISAdmin):
    list_display = (
        "id",
        "name",
        "centroid",
    )