from rest_framework import serializers
from .base_resource import ResourceSerializer


class WigleSerializer(ResourceSerializer):
    
    ssid = serializers.CharField(max_length=256)
    trilat = serializers.FloatField()
    trilong = serializers.FloatField()
    type = serializers.CharField(max_length=20)
