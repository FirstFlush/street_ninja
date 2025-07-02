from django.contrib import admin
from street_ninja_server.base_admin import BaseGISAdmin
from .models import Shelter, FoodProgram, Toilet, DrinkingFountain, PublicWifi


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


@admin.register(FoodProgram)
class FoodProgramAdmin(BaseGISAdmin):
    list_display = (
        'program_name',
        'organization_name',
        'program_status',
        'provides_meals',
        'provides_hampers',
        'signup_required',
        'requires_referral',
        'last_fetched',
        'date_created',
    )
    list_filter = (
        'provides_meals', 
        'provides_hampers',
        'delivery_available',
        'takeout_available', 
        'signup_required', 
        'requires_referral'
    )
    search_fields = ('program_name', 'organization_name', 'location_address')
    ordering = ('-last_fetched',)

    map_template = 'gis/admin/openlayers.html'
    default_lon = -123.116226
    default_lat = 49.246292
    default_zoom = 12


@admin.register(Toilet)
class ToiletAdmin(BaseGISAdmin):
    list_display = (
        'name',
        'address',
        'dataset',
        'is_wheelchair',
        'summer_hours',
        'winter_hours',
        'last_fetched',
        'date_created',
    )
    list_filter = ('dataset', 'is_wheelchair')
    search_fields = ('name', 'address', 'description')
    ordering = ('-last_fetched',)

    map_template = 'gis/admin/openlayers.html'
    default_lon = -123.116226
    default_lat = 49.246292
    default_zoom = 12


@admin.register(DrinkingFountain)
class DrinkingFountainAdmin(BaseGISAdmin):
    list_display = (
        'name',
        'in_operation',
        'pet_friendly',
        'last_fetched',
        'date_created',
    )
    list_filter = ('in_operation', 'pet_friendly')
    search_fields = ('name',)
    ordering = ('-last_fetched',)

    map_template = 'gis/admin/openlayers.html'
    default_lon = -123.116226
    default_lat = 49.246292
    default_zoom = 12


@admin.register(PublicWifi)
class PublicWifiAdmin(BaseGISAdmin):
    list_display = (
        'ssid',
        'name',
        'address',
        'last_fetched',
        'date_created',
    )
    search_fields = ('ssid', 'address',)
    ordering = ('-last_fetched',)

    map_template = 'gis/admin/openlayers.html'
    default_lon = -123.116226
    default_lat = 49.246292
    default_zoom = 12
