from dataclasses import asdict
from rest_framework import serializers
from common.enums import SMSKeywordEnum
from common.serializer_fields import YesNoBooleanField
from .dataclasses import MapPoint, MapData


class MapPointSerializer(serializers.Serializer):
    # type = serializers.ChoiceField(choices=["shelter", "food", "water", "toilet", "wifi"])
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    # name = serializers.CharField(allow_null=True, required=False)

    def to_representation(self, instance: MapPoint):
        """Convert MapPoint dataclass to JSON"""
        return asdict(instance)


class MapDataSerializer(serializers.Serializer):
    data = serializers.DictField(
        child=MapPointSerializer(many=True),
    )

    def validate_data(self, value):
        """Ensure only allowed resource types exist in the dictionary."""
        allowed_keys = set([value.lower() for value in SMSKeywordEnum.values])
        invalid_keys = set(value.keys()) - allowed_keys
        if invalid_keys:
            raise serializers.ValidationError(f"Invalid resource types: {', '.join(invalid_keys)}")

        return value

    def to_representation(self, instance: MapData):
        """Convert MapData dataclass to JSON"""
        return asdict(instance)




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


