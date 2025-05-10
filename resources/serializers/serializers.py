# from dataclasses import asdict
# from rest_framework import serializers
# from sms.enums import SMSKeywordEnum
# from common.serializer_fields import YesNoBooleanField
# from ..dataclasses import MapPoint, MapData


# class MapPointSerializer(serializers.Serializer):
#     longitude = serializers.FloatField()
#     latitude = serializers.FloatField()

#     def to_representation(self, instance: MapPoint):
#         """Convert MapPoint dataclass to JSON"""
#         return asdict(instance)


# class MapDataSerializer(serializers.Serializer):
#     data = serializers.DictField(
#         child=MapPointSerializer(many=True),
#     )

#     def validate_data(self, value):
#         """Ensure only allowed resource types exist in the dictionary."""
#         allowed_keys = set([value.lower() for value in SMSKeywordEnum.values])
#         invalid_keys = set(value.keys()) - allowed_keys
#         if invalid_keys:
#             raise serializers.ValidationError(f"Invalid resource types: {', '.join(invalid_keys)}")
#         return value

#     def to_representation(self, instance: MapData):
#         """Convert MapData dataclass to JSON"""
#         return asdict(instance)


# class DirectionsSerializer(serializers.Serializer):

#     instruction = serializers.CharField()
#     distance = serializers.FloatField()






# class ResourceSerializer(serializers.Serializer):
#     """Base class for all Resource model serializers. Primarly for type-hinting."""
#     ...


# class CityOfVancouverSerializer(ResourceSerializer):
#     ...


# class WigleSerializer(ResourceSerializer):
    
#     ssid = serializers.CharField(max_length=256)
#     trilat = serializers.FloatField()
#     trilong = serializers.FloatField()
#     type = serializers.CharField(max_length=20)


# class GeoPointSerializer(ResourceSerializer):
#     lon = serializers.FloatField()
#     lat = serializers.FloatField()

#     def validate_lon(self, value):
#         if not -180 <= value <= 180:
#             raise serializers.ValidationError("Longitude must be between -180 and 180.")
#         return value

#     def validate_lat(self, value):
#         if not -90 <= value <= 90:
#             raise serializers.ValidationError("Latitude must be between -90 and 90.")
#         return value

# class ShelterSerializer(CityOfVancouverSerializer):
#     facility    = serializers.CharField(max_length=256)
#     geo_point_2d = GeoPointSerializer()
#     category = serializers.CharField(max_length=24)
#     phone = serializers.CharField(max_length=20)
#     meals = YesNoBooleanField()
#     pets = YesNoBooleanField()
#     carts = YesNoBooleanField()


# class FoodProgramSerializer(CityOfVancouverSerializer):
    
#     program_name = serializers.CharField(max_length=256)
#     description = serializers.CharField(allow_null=True, required=False)
#     program_status = serializers.CharField(max_length=256)
#     organization_name = serializers.CharField(max_length=256)
#     geom = GeoPointSerializer()
#     location_address = serializers.CharField(max_length=256, allow_null=True, required=False)
#     address_extra_info = serializers.CharField(max_length=256, allow_null=True, required=False)
#     program_population_served = serializers.CharField(max_length=256, allow_null=True, required=False)
#     provides_meals = YesNoBooleanField()
#     provides_hampers = YesNoBooleanField()
#     delivery_available = YesNoBooleanField()
#     takeout_available = YesNoBooleanField()
#     wheelchair_accessible = YesNoBooleanField()
#     meal_cost = serializers.CharField(allow_null=True, required=False)
#     hamper_cost = serializers.CharField(allow_null=True, required=False)
#     signup_required = YesNoBooleanField()
#     signup_phone_number = serializers.CharField(max_length=20, allow_null=True, required=False)
#     signup_email = serializers.CharField(max_length=256, allow_null=True, required=False)
#     referral_agency_name = serializers.CharField(max_length=256, allow_null=True, required=False)
#     referral_phone_number = serializers.CharField(max_length=20, allow_null=True, required=False)
#     referral_email  = serializers.CharField(max_length=256, allow_null=True, required=False)
#     requires_referral = YesNoBooleanField()

#     def __new__(cls, *args, **kwargs):
#         """Filter out invalid records before DRF processes them"""
#         data = kwargs.get("data", None)
#         if isinstance(data, list):  
#             kwargs["data"] = [record for record in data if "geom" in record and record["geom"] is not None]
#         return super().__new__(cls, *args, **kwargs)


# class DrinkingFountainSerializer(CityOfVancouverSerializer):

#     name = serializers.CharField(max_length=256)
#     in_operation = serializers.CharField(max_length=64, allow_null=True, required=False)
#     pet_friendly = YesNoBooleanField(allow_null=True, required=False)
#     geo_point_2d = GeoPointSerializer()

#     def validate_in_operation(self, value):
#         return "Year Round" if value is None else value


# class PublicToiletSerializer(CityOfVancouverSerializer):

#     name = serializers.CharField(max_length=256)
#     address = serializers.CharField(max_length=256)
#     location = serializers.CharField(max_length=256, allow_null=True, required=False)
#     summer_hours = serializers.CharField()
#     winter_hours = serializers.CharField()
#     wheel_access = YesNoBooleanField()
#     geo_point_2d = GeoPointSerializer()


#     def validate(self, attrs):
#         attrs['dataset'] = 'public'
#         attrs['notes'] = attrs.pop('location')
#         attrs['is_wheelchair'] = attrs.pop('wheel_access')
#         return attrs


#     def run_validation(self, data):
#         """Preprocess the raw data list before field validation"""
#         if isinstance(data.get("wheel_access"), str) and data["wheel_access"].strip().lower() == "yes, entered from parking lot level":
#             data["wheel_access"] = "yes" 
#         return super().run_validation(data)

