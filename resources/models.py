from django.db import models
from django.contrib.gis.db import models as gis_models
from .enums import ShelterCategoryParamValue
from .abstract_models import CityOfVancouverModel, WigleModel


class Shelter(CityOfVancouverModel):

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

    def __str__(self) -> str:
        return self.facility


class FoodProgram(CityOfVancouverModel):

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

# class Toilets(CityOfVancouverModel):
#     address = models.CharField(max_length=256, unique=True)
#     location = gis_models.PointField(srid=4326)
    # is_active = models.BooleanField(default=True)

class DrinkingFountain(CityOfVancouverModel):
    name = models.CharField(max_length=256)
    location = gis_models.PointField(srid=4326)
    is_active = models.BooleanField(default=True)
    in_operation = models.CharField(max_length=64, default="year-round")
    pet_friendly = models.BooleanField(null=True)
    last_fetched = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

# class PublicWifi(WigleModel):    
#     address = models.CharField(max_length=256, unique=True)
#     location = gis_models.PointField(srid=4326)
    # is_active = models.BooleanField(default=True)