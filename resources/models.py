from django.db import models
from django.contrib.gis.db import models as gis_models
from .base_model import ResourceModel
from .enums import ShelterCategoryEnum


class Shelter(ResourceModel):

    name = models.CharField(max_length=256, unique=True)
    address = models.CharField(max_length=256, unique=True)
    location = gis_models.PointField(srid=4326)
    category = models.CharField(max_length=24, choices=ShelterCategoryEnum.choices)
    phone = models.CharField(max_length=20, unique=True)
    meals = models.BooleanField()
    pets = models.BooleanField()
    carts = models.BooleanField()
    last_updated = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)


class FoodProgram(ResourceModel):
    
    program_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=256, unique=True)
    address_extra_info = models.CharField(max_length=256)
    description = models.TextField()
    location = gis_models.PointField(srid=4326)
    provides_meals = models.BooleanField()
    provides_hampers = models.BooleanField()
    meal_cost = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    hamper_cost = models.DecimalField(decimal_places=2, max_digits=7, null=True)
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
    last_updated = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

# class Toilets(ResourceModel):
#     address = models.CharField(max_length=256, unique=True)
#     location = gis_models.PointField(srid=4326)


# class DrinkingFountain(ResourceModel):
#     address = models.CharField(max_length=256, unique=True)
#     location = gis_models.PointField(srid=4326)


# class PublicWifi(ResourceModel):    
#     address = models.CharField(max_length=256, unique=True)
#     location = gis_models.PointField(srid=4326)