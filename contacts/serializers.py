from rest_framework import serializers
from .enums import ContactMethodEnum


class ContactSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=256)
    organization = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(max_length=256)
    phone = serializers.CharField(max_length=20, min_length=10)
    contactMethod = serializers.ChoiceField(choices=ContactMethodEnum.values)
    msg = serializers.CharField()