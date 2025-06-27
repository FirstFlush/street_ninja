from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from typing import Any
from sms.enums import SMSKeywordEnum
from sms.resolvers.params.param_mappings.shelter import ShelterCategoryParamValue
from .abstract_models import CityOfVancouverModel, WigleModel


class Shelter(CityOfVancouverModel):

    _keyword_enum = SMSKeywordEnum.SHELTER
    _unique_key = "facility"

    facility = models.CharField(max_length=256, unique=True)
    address = models.CharField(max_length=256)
    location = gis_models.PointField(srid=4326)
    category = models.CharField(max_length=24, choices=ShelterCategoryParamValue.choices)
    phone = models.CharField(max_length=20, unique=True)
    meals = models.BooleanField()
    pets = models.BooleanField()
    carts = models.BooleanField()
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def resource_name(self) -> str:
        return self.facility

    def __str__(self) -> str:
        return self.facility


class FoodProgram(CityOfVancouverModel):

    _keyword_enum = SMSKeywordEnum.FOOD
    _unique_key = "program_name"

    program_name = models.CharField(max_length=256, unique=True)
    program_status = models.CharField(max_length=20)
    program_population_served = models.TextField(null=True)
    organization_name = models.CharField(max_length=256)
    location_address = models.CharField(max_length=256, null=True)
    address_extra_info = models.CharField(max_length=256, null=True)
    description = models.TextField(null=True)
    location = gis_models.PointField(srid=4326)
    provides_meals = models.BooleanField()
    provides_hampers = models.BooleanField()
    meal_cost = models.CharField(max_length=20, null=True)
    hamper_cost = models.CharField(max_length=20, null=True)
    delivery_available = models.BooleanField()
    takeout_available = models.BooleanField()
    wheelchair_accessible = models.BooleanField()
    signup_required = models.BooleanField()
    signup_phone_number = models.CharField(max_length=20, null=True)
    signup_email = models.CharField(max_length=256, null=True)
    requires_referral = models.BooleanField()
    referral_agency_name = models.CharField(max_length=256, null=True) 
    referral_phone_number = models.CharField(max_length=20, null=True)
    referral_email = models.CharField(max_length=256, null=True)
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def resource_name(self) -> str:
        return self.program_name
    

class Toilet(CityOfVancouverModel):

    DATASET_CHOICES = (
        ('public', 'Public'),
        ('parks', 'Parks'),
    )
    _keyword_enum = SMSKeywordEnum.TOILET
    

    name = models.CharField(max_length=256, null=True)
    address = models.CharField(max_length=256, null=True)
    dataset = models.CharField(max_length=256, choices=DATASET_CHOICES)
    description = models.CharField(max_length=256, null=True)
    location = gis_models.PointField(srid=4326)
    notes = models.TextField(null=True)
    summer_hours = models.CharField(max_length=64, null=True)
    winter_hours = models.CharField(max_length=64, null=True)
    is_wheelchair = models.BooleanField()
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def resource_name(self) -> str:
        return self.name


class DrinkingFountain(CityOfVancouverModel):

    _keyword_enum = SMSKeywordEnum.WATER
    _unique_key = "location"

    name = models.CharField(max_length=256)
    location = gis_models.PointField(srid=4326)
    is_active = models.BooleanField(default=True)
    in_operation = models.CharField(max_length=64, default="year-round")
    pet_friendly = models.BooleanField(null=True)
    last_fetched = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def resource_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class PublicWifi(WigleModel):

    _keyword_enum = SMSKeywordEnum.WIFI
    _unique_key = "location"
    
    name = models.CharField(max_length=256, default="", blank=True)
    address = models.CharField(max_length=256, default="", blank=True)
    ssid = models.CharField(max_length=256)
    location = gis_models.PointField(srid=4326)
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ssid", "location", "name", "address"],
                name="unique_ssid_location_name_address",
            )
        ]

    @property
    def resource_name(self) -> str:
        return self.ssid

    def __str__(self) -> str:
        location: Point = self.location # becuase pylance is not recognizing self.location as Point object! 
        return f"{self.ssid}: {location.x}, {location.y}"