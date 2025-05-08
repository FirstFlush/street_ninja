from rest_framework import serializers


class WebSMSSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3, max_length=256)


class TwilioSMSSerializer(serializers.Serializer):

    MessageSid = serializers.CharField(max_length=34, min_length=34)
    From = serializers.CharField(max_length=20)
    Body = serializers.CharField(max_length=256)