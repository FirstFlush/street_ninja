from rest_framework import serializers


class NeighborhoodSerializer(serializers.Serializer):

    name = serializers.CharField()
    coordinates = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(), min_length=2, max_length=2
        )
    )
