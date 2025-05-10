from rest_framework import serializers


class DirectionsSerializer(serializers.Serializer):

    instruction = serializers.CharField()
    distance = serializers.FloatField()


