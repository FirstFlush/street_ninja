from rest_framework import serializers
from common.serializer_fields import YesNoBooleanField


class ResourceSerializer(serializers.Serializer):
    """Base class for all Resource model serializers. Primarly for type-hinting."""
    ...


class GeoPointSerializer(ResourceSerializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()

    def validate_lon(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def validate_lat(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

class ShelterSerializer(ResourceSerializer):
    facility = serializers.CharField(max_length=256)
    geo_point_2d = GeoPointSerializer()
    category = serializers.CharField(max_length=24)
    phone = serializers.CharField(max_length=20)
    meals = YesNoBooleanField()
    pets = YesNoBooleanField()
    carts = YesNoBooleanField()


