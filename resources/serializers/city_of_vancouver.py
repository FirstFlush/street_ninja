from rest_framework import serializers
from .base_resource import ResourceSerializer, GeoPointSerializer
from common.serializer_fields import YesNoBooleanField


class CityOfVancouverSerializer(ResourceSerializer):
    ...


class ShelterSerializer(CityOfVancouverSerializer):
    facility    = serializers.CharField(max_length=256)
    geo_point_2d = GeoPointSerializer()
    category = serializers.CharField(max_length=24)
    phone = serializers.CharField(max_length=20)
    meals = YesNoBooleanField()
    pets = YesNoBooleanField()
    carts = YesNoBooleanField()


class FoodProgramSerializer(CityOfVancouverSerializer):
    
    program_name = serializers.CharField(max_length=256)
    description = serializers.CharField(allow_null=True, required=False)
    program_status = serializers.CharField(max_length=256)
    organization_name = serializers.CharField(max_length=256)
    geom = GeoPointSerializer()
    location_address = serializers.CharField(max_length=256, allow_null=True, required=False)
    address_extra_info = serializers.CharField(max_length=256, allow_null=True, required=False)
    program_population_served = serializers.CharField(max_length=256, allow_null=True, required=False)
    provides_meals = YesNoBooleanField()
    provides_hampers = YesNoBooleanField()
    delivery_available = YesNoBooleanField()
    takeout_available = YesNoBooleanField()
    wheelchair_accessible = YesNoBooleanField()
    meal_cost = serializers.CharField(allow_null=True, required=False)
    hamper_cost = serializers.CharField(allow_null=True, required=False)
    signup_required = YesNoBooleanField()
    signup_phone_number = serializers.CharField(max_length=20, allow_null=True, required=False)
    signup_email = serializers.CharField(max_length=256, allow_null=True, required=False)
    referral_agency_name = serializers.CharField(max_length=256, allow_null=True, required=False)
    referral_phone_number = serializers.CharField(max_length=20, allow_null=True, required=False)
    referral_email  = serializers.CharField(max_length=256, allow_null=True, required=False)
    requires_referral = YesNoBooleanField()

    def __new__(cls, *args, **kwargs):
        """Filter out invalid records before DRF processes them"""
        data = kwargs.get("data", None)
        if isinstance(data, list):  
            kwargs["data"] = [record for record in data if "geom" in record and record["geom"] is not None]
        return super().__new__(cls, *args, **kwargs)


class DrinkingFountainSerializer(CityOfVancouverSerializer):

    name = serializers.CharField(max_length=256)
    in_operation = serializers.CharField(max_length=64, allow_null=True, required=False)
    pet_friendly = YesNoBooleanField(allow_null=True, required=False)
    geo_point_2d = GeoPointSerializer()

    def validate_in_operation(self, value):
        return "Year Round" if value is None else value


class PublicToiletSerializer(CityOfVancouverSerializer):

    name = serializers.CharField(max_length=256, allow_null=True, required=False)
    address = serializers.CharField(max_length=256, allow_null=True, required=False)
    location = serializers.CharField(max_length=256, allow_null=True, required=False)
    summer_hours = serializers.CharField()
    winter_hours = serializers.CharField()
    wheel_access = YesNoBooleanField()
    geo_point_2d = GeoPointSerializer()


    def validate(self, attrs):
        attrs['dataset'] = 'public'
        attrs['notes'] = attrs.pop('location')
        attrs['is_wheelchair'] = attrs.pop('wheel_access')
        return attrs


    def run_validation(self, data):
        """Preprocess the raw data list before field validation"""
        if isinstance(data.get("wheel_access"), str) and data["wheel_access"].strip().lower() == "yes, entered from parking lot level":
            data["wheel_access"] = "yes" 
        return super().run_validation(data)

