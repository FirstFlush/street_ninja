from ..dataclasses import MapPoint, MapData
from rest_framework import serializers
from sms.enums import SMSKeywordEnum
from dataclasses import asdict


class MapPointSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

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
