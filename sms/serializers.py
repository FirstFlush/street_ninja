from rest_framework import serializers


class TwilioSMSSerializer(serializers.Serializer):

    MessageSid = serializers.CharField(max_length=34, min_length=34)
    From = serializers.CharField(max_length=20)
    Body = serializers.CharField(max_length=1600)